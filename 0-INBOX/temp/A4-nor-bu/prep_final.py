"""Outline fix (P5): sun/moon (vimana) and Meru subtrees belong to the Four Great Kings
(-1-1), not to the 33 gods (-1-2). Rename their IDs (same depth) and move the 33-gods
heading after them. Also merge all part anchors into parts-final/P0/anchors.tsv."""
import re, sys, glob, os
src, pre, outdir = sys.argv[1:4]
OLD = "2-2-2-2-2-2-3-2-1-3-1-2-2-1-2-"; NEW = "2-2-2-2-2-2-3-2-1-3-1-2-2-1-1-"
G33 = "2-2-2-2-2-2-3-2-1-3-1-2-2-1-2-0"; NEXT = "2-2-2-2-2-2-3-2-1-3-1-2-2-2-0"
ren = lambda i: NEW + i[len(OLD):] if i.startswith(OLD) and i != G33 else i
raw = open(src, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
L = raw.split(nl)
H = re.compile(r"^(#+\s+.*?\s*\^)([\w-]+)(\s*)$")
g33 = None; out = []
for l in L:
    m = H.match(l)
    if m and m.group(2) == G33:
        g33 = l; out.append(None); continue
    if m: l = m.group(1) + ren(m.group(2)) + m.group(3)
    if m and m.group(2) == NEXT:
        out += [g33, ""]
    out.append(l)
i = out.index(None); del out[i]
if out[i] == "": del out[i]          # the blank line after the moved heading
open(pre, "w", encoding="utf-8", newline="").write(nl.join(out))
os.makedirs(outdir, exist_ok=True)
rows = ["id\tblock\tanchor\tconfidence\tnote"]
for f in sorted(glob.glob("parts/P*/anchors.tsv")):
    for ln in open(f, encoding="utf-8").read().splitlines()[1:]:
        c = ln.split("\t")
        if not c[0].strip(): continue
        if c[0] == G33:
            c = [G33, "2-356", "གཉིས་པ་སུམ་ཅུ་རྩ་གསུམ་པའི་གནས་སྟོན་པ་ནི།", "high", "own opener, after the Four Kings' two parts (outline fix)"]
        c[0] = ren(c[0]); rows.append("\t".join(c))
open(os.path.join(outdir, "anchors.tsv"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
print("renamed", sum(1 for l in L if (m := H.match(l)) and ren(m.group(2)) != m.group(2)), "rows", len(rows) - 1)
