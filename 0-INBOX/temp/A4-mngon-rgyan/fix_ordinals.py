"""A.5 sibling ordinals, majority rule (priority_repo.md §A.5). Heading lines only; IDs and text unchanged.
Within a group of numeric siblings: more than half carry an ordinal -> add the matching one to the rest;
fewer than half -> strip from the few; tie -> file habit (uniform-with >= uniform-without -> add);
a heading whose title is only an ordinal is never stripped (its group gets ordinals added instead).
A title that already contains its own ordinal word inside (e.g. གནས་བརྒྱད་ལས་དང་པོ་…) counts as having one.
usage: fix_ordinals.py IN_MD OUT_MD
"""
import re, sys, collections
inp, outp = sys.argv[1:3]
WORD = {1: "དང་པོ", 2: "གཉིས་པ", 3: "གསུམ་པ", 4: "བཞི་པ", 5: "ལྔ་པ", 6: "དྲུག་པ", 7: "བདུན་པ", 8: "བརྒྱད་པ",
        9: "དགུ་པ", 10: "བཅུ་པ", 11: "བཅུ་གཅིག་པ", 12: "བཅུ་གཉིས་པ", 13: "བཅུ་གསུམ་པ", 14: "བཅུ་བཞི་པ",
        15: "བཅོ་ལྔ་པ", 16: "བཅུ་དྲུག་པ", 17: "བཅུ་བདུན་པ", 18: "བཅོ་བརྒྱད་པ", 19: "བཅུ་དགུ་པ", 20: "ཉི་ཤུ་པ"}
STEMS = sorted([(w[:-2] if w.endswith("་པ") else w) for w in WORD.values()], key=len, reverse=True)
H = re.compile(r"^(#+)(\s+)(.*?)(\s*\^)([\w-]+)(\s*)$")

def lead_ordinal(t):
    """ordinal word at the start (with its ་པ/་བ/པོ form), returns the prefix to strip incl. trailing tsheg"""
    for s in STEMS:
        for suf in ("", "་པ", "་བ"):
            w = s + suf if s != "དང་པོ" else s
            if t.startswith(w) and (len(t) == len(w) or t[len(w)] in "་།རསའ "):
                if s != "དང་པོ" and suf == "":
                    continue
                k = len(w)
                return t[:k + 1] if k < len(t) and t[k] == "་" else t[:k]
    return None

L = open(inp, encoding="utf-8", newline="").read().split("\n")
heads = []
for i, l in enumerate(L):
    m = H.match(l)
    if m and m.group(5) != "0":
        raw = m.group(3); bold = raw.startswith("**") and raw.endswith("**")
        title = raw.strip("*").strip()
        segs = m.group(5).split("-")
        heads.append(dict(i=i, m=m, bold=bold, title=title, segs=segs))
groups = collections.defaultdict(list)
for h in heads:
    if len(h["segs"]) >= 2 and h["segs"][-2].isdigit():
        groups[tuple(h["segs"][:-2])].append(h)
def has(h):
    n = int(h["segs"][-2]); w = WORD.get(n, "")
    return bool(lead_ordinal(h["title"])) or bool(w and re.search(re.escape(w) + "(?![ཱ-྄])", h["title"][:40]))
with_u = without_u = 0
mixed = []
for par, ks in groups.items():
    if len(ks) < 2: continue
    k = sum(has(h) for h in ks)
    if k == len(ks): with_u += 1
    elif k == 0: without_u += 1
    else: mixed.append((par, ks, k))
changes = []
for par, ks, k in mixed:
    n = len(ks)
    add = k * 2 > n or (k * 2 == n and with_u >= without_u)
    bare = [h for h in ks if has(h) and lead_ordinal(h["title"]) and h["title"][len(lead_ordinal(h["title"])):].strip("།་ ") == ""]
    if not add and bare: add = True
    for h in ks:
        t = h["title"]
        if add and not has(h):
            new = WORD[int(h["segs"][-2])] + "་" + t
        elif not add and has(h) and lead_ordinal(t):
            new = t[len(lead_ordinal(t)):]
        else:
            continue
        m = h["m"]
        disp = f"**{new}**" if h["bold"] else new
        L[h["i"]] = m.group(1) + m.group(2) + disp + m.group(4) + m.group(5) + m.group(6)
        changes.append(f"{'ADD  ' if add else 'STRIP'} ^{m.group(5)}: {t}  →  {new}")
open(outp, "w", encoding="utf-8", newline="").write("\n".join(L))
print(f"mixed groups {len(mixed)}; headings changed {len(changes)} (uniform with/without: {with_u}/{without_u})")
print("\n".join(changes))
