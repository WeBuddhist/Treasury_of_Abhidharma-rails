"""Move headings to the anchors in parts/P*/anchors.tsv, cutting blocks there.

usage: apply_anchors.py SOURCE PARTS_DIR OUT_MD REPORT [--drop ID,ID…]
The text is never changed: a block is only cut into pieces; each piece keeps
its characters and gets ' ^ID'. Body IDs are renumbered per ## label.
Headings whose anchor is NONE stay just after the previous heading unless
listed in --drop.
"""
import re, sys, glob, os, collections, argparse

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("parts"); ap.add_argument("out"); ap.add_argument("report")
ap.add_argument("--drop", default="")
a = ap.parse_args()
drop = set(x for x in a.drop.split(",") if x)

raw = open(a.src, encoding="utf-8", newline="").read()
crlf = "\r\n" in raw
raw = raw.replace("\r\n", "\n")
fm = re.match(r"\A---\n.*?\n---\n", raw, flags=re.S)
head_txt, body = raw[:fm.end()], raw[fm.end():]
lines = body.split("\n")
H = re.compile(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$")
IDT = re.compile(r"(\s*)\^([\w-]+)\s*$")
WS = " \t 　"

items, cur = [], []
def flush():
    global cur
    if cur:
        last = lines[cur[-1]]; m = IDT.search(last)
        txt = "\n".join(lines[i] for i in cur)
        core = txt[: len(txt) - len(last) + m.start()]
        items.append(("B", dict(text=core, sep=m.group(1), id=m.group(2), orig=txt)))
        cur = []
for i, l in enumerate(lines):
    m = H.match(l)
    if m:
        flush()
        items.append(("H", dict(level=len(m.group(1)), raw=l, title=m.group(2).strip("*").strip(),
                                id=m.group(3), segs=m.group(3).split("-"))))
    elif l.strip() == "": flush()
    else: cur.append(i)
flush()
blocks = [it for k, it in items if k == "B"]
bnum = {b["id"]: n for n, b in enumerate(blocks)}
heads = [it for k, it in items if k == "H"]
cur_pos = {}
n = 0
for k, it in items:
    if k == "B": n += 1
    else: cur_pos[it["id"]] = (n, 0)

anc = {}
for f in sorted(glob.glob(os.path.join(a.parts, "P*", "anchors.tsv"))):
    for ln in open(f, encoding="utf-8").read().splitlines()[1:]:
        c = ln.split("\t")
        if len(c) < 3 or not c[0].strip(): continue
        anc[c[0].strip()] = dict(block=c[1].strip().lstrip("^"), anchor=c[2].strip(),
                                 conf=(c[3].strip() if len(c) > 3 else ""), note=(c[4].strip() if len(c) > 4 else ""),
                                 part=os.path.basename(os.path.dirname(f)))

def rx(anchor):
    parts = re.split(r"[\s ]+", anchor.strip())
    return re.compile(r"[\s ]*".join(re.escape(p) for p in parts if p))

def clause_ok(tx, p):
    q = p
    while q > 0 and tx[q - 1] in WS: q -= 1
    return q == 0 or tx[q - 1] in "།༔༏༐༑"

LEAD = re.compile(r"^[༄༅༆།​﻿" + WS + "]*")   # zero-width chars count as lead marks: never leave a piece of only those
rep = collections.defaultdict(list)
pos = {}
prev = (0, 0)
for h in heads:
    hid = h["id"]
    if hid == "0": pos[hid] = cur_pos[hid]; prev = pos[hid]; continue
    r = anc.get(hid)
    if r is None:
        rep["no row"].append(hid); pos[hid] = max(prev, cur_pos[hid]); prev = pos[hid]; continue
    if r["anchor"].upper() == "NONE":
        rep["NONE"].append(f"{hid} [{r['part']}] {h['title']} — {r['note']}")
        pos[hid] = prev; continue
    pat = rx(r["anchor"])
    found = None
    order = [bnum[r["block"]]] if r["block"] in bnum else []
    if order:
        b0 = order[0]; order += [b for d in (1, -1, 2, -2, 3, -3) for b in [b0 + d] if 0 <= b < len(blocks)]
    else:
        order = range(prev[0], len(blocks))
    for b in order:
        tx = blocks[b]["text"]
        for m in pat.finditer(tx):
            p = m.start()
            if p <= LEAD.match(tx).end(): p = 0
            if (b, p) >= prev:
                found = (b, p); break
        if found: break
    if not found:
        rep["anchor not found (kept after previous)"].append(f"{hid} [{r['part']}] block {r['block']}: {r['anchor']}")
        pos[hid] = prev; continue
    if found[0] != bnum.get(r["block"]):
        rep["found in another block"].append(f"{hid}: said {r['block']}, found {blocks[found[0]]['id']}")
    if found[1] and not clause_ok(blocks[found[0]]["text"], found[1]):
        rep["cut not at a clause boundary"].append(f"{hid}: …{blocks[found[0]]['text'][max(0,found[1]-25):found[1]+25]}…")
    pos[hid] = found; prev = found
    if r["conf"] in ("low", "medium"):
        rep[f"{r['conf']} confidence"].append(f"{hid} [{r['part']}] {h['title']} — {r['note']}")

# rebuild
cuts = collections.defaultdict(set)
at = collections.defaultdict(list)
for h in heads:
    if h["id"] in drop: rep["dropped"].append(h["id"] + " " + h["title"]); continue
    b, o = pos[h["id"]]
    if o: cuts[b].add(o)
    at[(b, o)].append(h)
out = []
for b, blk in enumerate(blocks):
    offs = sorted({0} | cuts.get(b, set()))
    for q, o in enumerate(offs):
        out += [("H", h) for h in at.get((b, o), [])]
        end = offs[q + 1] if q + 1 < len(offs) else len(blk["text"])
        out.append(("P", dict(text=blk["text"][o:end], last=q + 1 == len(offs), blk=blk, single=len(offs) == 1)))
for (b, o), hs in at.items():
    if b >= len(blocks): out += [("H", h) for h in hs]
label, cnt, final, idmap = None, collections.Counter(), [], []
for k, it in out:
    if k == "H":
        if it["level"] == 1: label = "0"
        if it["level"] == 2: label = it["segs"][0]
        final.append(it["raw"]); continue
    cnt[label] += 1
    nid = f"{label}-{cnt[label]}"
    idmap.append((it["blk"]["id"], nid))
    if it["single"] and nid == it["blk"]["id"]:
        final.append(it["blk"]["orig"])
    else:
        txt = it["text"]
        if it["last"]:
            final.append(txt + it["blk"]["sep"] + "^" + nid)
        else:   # keep the piece's own trailing NBSP etc.; one plain space before the ID
            txt = txt.rstrip("\n")
            final.append(txt + " ^" + nid)   # keep the piece's own trailing space/NBSP as text
text = head_txt + "\n" + "\n\n".join(final) + "\n"
if crlf: text = text.replace("\n", "\r\n")
open(a.out, "w", encoding="utf-8", newline="").write(text)

# text gate: body characters identical (ignoring headings, IDs, whitespace)
def letters(s):
    s = re.sub(r"(?m)^#.*$", "", s.replace("\r\n", "\n"))
    s = re.sub(r"\^[\w-]+", "", s)
    return re.sub(r"[\s ]+", "", s)
same = letters(body) == letters(text[len(head_txt):])
changed = sum(1 for o, nn in idmap if o != nn)
with open(a.report, "w", encoding="utf-8") as w:
    w.write(f"text identical (letters): {same}\nblocks {len(blocks)} -> {len(idmap)}; cuts {sum(len(v) for v in cuts.values())}; body IDs changed {changed}\n\n")
    for k, v in rep.items():
        w.write(f"## {k} ({len(v)})\n" + "".join(f"- {x}\n" for x in v) + "\n")
    w.write("## old -> new block IDs\n" + "".join(f"{o}\t{nn}\n" for o, nn in idmap))
print(f"text identical: {same}; blocks {len(blocks)} -> {len(idmap)}; IDs changed {changed}")
for k, v in rep.items(): print(f"  {k}: {len(v)}")
