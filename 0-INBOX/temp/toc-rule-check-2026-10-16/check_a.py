"""Check a source file against priority_repo.md §A (A.1-A.5). Read-only.
usage: check_a.py FILE
"""
import re, sys, collections, pathlib

ORD = [("བཅུ་གཅིག", 11), ("བཅུ་གཉིས", 12), ("བཅུ་གསུམ", 13), ("བཅུ་བཞི", 14), ("བཅོ་ལྔ", 15),
       ("བཅུ་དྲུག", 16), ("བཅུ་བདུན", 17), ("བཅོ་བརྒྱད", 18), ("བཅུ་དགུ", 19), ("ཉི་ཤུ", 20),
       ("དང་པོ", 1), ("གཉིས", 2), ("གསུམ", 3), ("བཞི", 4), ("ལྔ", 5), ("དྲུག", 6), ("བདུན", 7),
       ("བརྒྱད", 8), ("དགུ", 9), ("བཅུ", 10)]
VOW = set(chr(c) for c in range(0x0F71, 0x0F85))
H = re.compile(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$")


def ordinal(title):
    t = title.lstrip("༄༅། ")
    for pre in ("", "གནས་", "ལེའུ་"):
        if not t.startswith(pre): continue
        s = t[len(pre):]
        for w, n in ORD:
            if w == "དང་པོ":
                if s.startswith(w) and (len(s) == len(w) or s[len(w)] in "་།༔ རསའ"): return n, pre + w
                continue
            for suf in ("་པ", "་བ"):
                ww = w + suf
                if s.startswith(ww) and (len(s) == len(ww) or s[len(ww)] in "་།༔ རསའ"):
                    return n, pre + ww
    return None


f = sys.argv[1]
raw = pathlib.Path(f).read_text(encoding="utf-8").replace("\r\n", "\n")
fm = re.match(r"\A---\n.*?\n---\n", raw, flags=re.S)
off = raw[:fm.end()].count("\n") if fm else 0
lines = raw[fm.end():].split("\n") if fm else raw.split("\n")

issues = collections.defaultdict(list)
heads = []
for i, l in enumerate(lines):
    if not l.startswith("#"): continue
    ln = i + 1 + off
    m = H.match(l)
    if not m:
        issues["A.3 heading without block ID"].append(f"L{ln} {l[:70]}"); continue
    level, title, hid = len(m.group(1)), m.group(2), m.group(3)
    segs = hid.split("-")
    bold = title.startswith("**") and title.endswith("**") and len(title) > 4
    plain = title.strip("*").strip()
    heads.append(dict(i=i, ln=ln, level=level, title=plain, id=hid,
                      path=tuple(segs[:-1]) if hid != "0" else (), segs=segs))
    # A.1
    depth = len(segs)
    if level != depth:
        issues["A.1 # count ≠ ID segments"].append(f"L{ln} {level}# vs ^{hid}")
    # A.2
    if level > 6 and not bold:
        issues["A.2 depth>6 not bold"].append(f"L{ln} ^{hid} {title[:50]}")
    if level <= 6 and "**" in title:
        issues["A.2 depth≤6 bold"].append(f"L{ln} ^{hid} {title[:50]}")
    if level > 6 and "**" in plain:
        issues["A.2 stray ** inside title"].append(f"L{ln} ^{hid} {title[:50]}")
    # A.3 -0
    if hid != "0" and segs[-1] != "0":
        issues["A.3 ID not ending -0"].append(f"L{ln} ^{hid}")

cnt = collections.Counter(h["id"] for h in heads)
for k, v in cnt.items():
    if v > 1: issues["A.3 duplicate ID"].append(f"^{k} ×{v}")
# body IDs colliding with heading IDs
body_ids = collections.Counter(re.findall(r"\s\^([\w-]+)\s*$", "\n".join(l for l in lines if not l.startswith("#")), flags=re.M))
for h in heads:
    if h["id"] in body_ids: issues["A.3 heading ID also used on a body block"].append(f"^{h['id']}")

seen = set()
kids = collections.defaultdict(list)
for k, h in enumerate(heads):
    if k and h["level"] > heads[k - 1]["level"] + 1:
        issues["A.3 level skip"].append(f"L{h['ln']} h{h['level']} after h{heads[k-1]['level']}")
    par = h["path"][:-1]
    if len(h["path"]) > 1 and par not in seen:
        issues["A.3 parent heading missing/after child"].append(f"L{h['ln']} ^{h['id']}")
    seen.add(h["path"])
    if h["path"]: kids[par].append(h)
    # A.4 empty section
    nxt = heads[k + 1] if k + 1 < len(heads) else None
    end = nxt["i"] if nxt else len(lines)
    between = "\n".join(lines[h["i"] + 1:end]).strip()
    if not between and (nxt is None or nxt["level"] <= h["level"]):
        issues["A.4 empty section"].append(f"L{h['ln']} ^{h['id']} {h['title'][:50]}")
    # A.5 ordinal vs ID
    o = ordinal(h["title"])
    h["ord"] = o
    if o and h["path"] and h["path"][-1].isdigit() and o[0] != int(h["path"][-1]):
        issues["A.5 title ordinal ≠ ID"].append(f"L{h['ln']} '{o[1]}'={o[0]} but ^{h['id']}: {h['title'][:50]}")

# sibling numbering + A.5 majority
groups_with = groups_without = 0
mixed = []
for par, ks in kids.items():
    num = [x for x in ks if x["path"][-1].isdigit()]
    nn = [int(x["path"][-1]) for x in num]
    if nn and nn != list(range(1, len(nn) + 1)):
        issues["sibling numbering gap/dup/order"].append(f"under {'-'.join(par) or 'root'}: {nn[:20]}")
    if len(num) < 2: continue
    w = [x for x in num if x["ord"]]
    if len(w) == len(num): groups_with += 1
    elif not w: groups_without += 1
    else: mixed.append((par, num, w))
for par, num, w in mixed:
    n, k = len(num), len(w)
    if k * 2 > n: dec = "ADD to the rest"
    elif k * 2 < n: dec = "STRIP from these few"
    else: dec = "TIE → file habit: " + ("ADD" if groups_with >= groups_without else "STRIP")
    bare = [x for x in w if x["title"].strip("།་ ") == x["ord"][1].strip("་")]
    if "STRIP" in dec and bare: dec += " (but a bare-ordinal title → ADD instead)"
    lacking = [x for x in num if not x["ord"]] if "ADD" in dec else w
    issues["A.5 mixed sibling ordinals"].append(
        f"under {'-'.join(par) or 'root'}: {k}/{n} with ordinal → {dec}; affects: " +
        "; ".join(f"L{x['ln']} ^{x['id']} {x['title'][:40]}" for x in lacking))

print(f"## {pathlib.Path(f).name}")
print(f"headings {len(heads)}, max depth {max(h['level'] for h in heads)}, "
      f"uniform sibling groups with/without ordinals {groups_with}/{groups_without}")
tot = sum(len(v) for v in issues.values())
print(f"ISSUES: {tot}")
for k, v in issues.items():
    print(f"### {k} ({len(v)})")
    for x in v: print("  -", x)
    if len(v) > 60: print(f"  … {len(v)-60} more")
