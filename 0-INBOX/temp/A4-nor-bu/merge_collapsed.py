"""In each COLLAPSE parent's own section, merge consecutive one-line (paragraph) blocks into one
block, then renumber body IDs per ## label and write an original -> final block map.
Verse blocks (several lines) stay separate. Text unchanged: blocks are joined with the
first block's trailing whitespace kept and one space if there was none.
usage: merge_collapsed.py IN_MD OUT_MD MAP_TSV ORIGINAL_MD
"""
import re, sys, glob
inp, outp, mapp, orig = sys.argv[1:5]
H = re.compile(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$")
IDT = re.compile(r" \^[\w-]+$")
collapse = set()
for f in glob.glob("collapse/C*/decisions.tsv"):
    for ln in open(f, encoding="utf-8").read().splitlines()[1:]:
        c = ln.split("\t")
        if len(c) > 1 and c[1].strip().upper() == "COLLAPSE": collapse.add(c[0].strip())
raw = open(inp, encoding="utf-8", newline="").read()
fm = re.match(r"\A---\n.*?\n---\n", raw, flags=re.S)
head, body = raw[:fm.end()], raw[fm.end():]
units = [u for u in body.strip("\n").split("\n\n")]       # headings and blocks, one per unit
out, cur_parent, merged = [], None, 0
for u in units:
    m = H.match(u)
    if m:
        cur_parent = m.group(3) if m.group(3) in collapse else None
        out.append(u); continue
    single = "\n" not in u
    if cur_parent and single and out and not H.match(out[-1]) and "\n" not in out[-1]:
        prev = IDT.sub("", out[-1])
        out[-1] = prev + u          # no added space: the text stays exactly as it was
        merged += 1
    else:
        out.append(u)
# renumber
label, cnt, final = None, {}, []
for u in out:
    m = H.match(u)
    if m:
        if len(m.group(1)) == 1: label = "0"
        elif len(m.group(1)) == 2: label = m.group(3).split("-")[0]
        final.append(u); continue
    cnt[label] = cnt.get(label, 0) + 1
    final.append(IDT.sub("", u) + " ^" + f"{label}-{cnt[label]}")
open(outp, "w", encoding="utf-8", newline="").write(head + "\n" + "\n\n".join(final) + "\n")

# original -> final map by character position (whitespace ignored)
def blocks(text):
    text = re.sub(r"\A---\n.*?\n---\n", "", text.replace("\r\n", "\n"), flags=re.S)
    res = []
    text = re.sub(r"(?m)^#.*$", "", text)
    for u in re.split(r"\n\s*\n", text.strip("\n")):
        if not u.strip(): continue
        m = re.search(r"\^([\w-]+)\s*$", u)
        res.append((m.group(1), len(re.sub(r"[\s ]+", "", re.sub(r"\^[\w-]+\s*$", "", u)))))
    return res
ob = blocks(open(orig, encoding="utf-8").read()); nb = blocks(open(outp, encoding="utf-8").read())
def spans(bl):
    s, r = 0, []
    for i, n in bl: r.append((i, s, s + n)); s += n
    return r
os_, ns_ = spans(ob), spans(nb)
with open(mapp, "w", encoding="utf-8") as w:
    w.write("old_id\tnew_ids\n")
    for oid, a, b in os_:
        w.write(oid + "\t" + ",".join(nid for nid, c, d in ns_ if c < b and d > a) + "\n")
print(f"merged {merged} blocks; blocks now {len(nb)} (original {len(ob)})")
