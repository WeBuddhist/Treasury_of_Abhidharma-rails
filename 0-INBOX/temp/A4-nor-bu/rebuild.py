"""Rebuild nor-bu from pre.md (backup + outline fix) with the drop set:
NONE headings + headings deeper than MAX_HASH + children of COLLAPSE groups.
usage: rebuild.py OUT_MD REPORT
"""
import re, sys, glob, subprocess, os
out_md, report = sys.argv[1:3]
MAX_HASH = 17          # parser TOC depth 16 (sa bcad levels under the # title)
NONE = ["2-2-2-2-2-2-2-3-1-2-%d-0" % i for i in range(1, 7)] + [
    "2-2-2-2-2-2-3-2-1-3-1-2-1-0", "2-2-2-2-2-2-4-2-1-2-3-2-3-1-1-1-2-0", "2-3-2-0"]
H = re.compile(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$")
hs = [(len(m.group(1)), m.group(3)) for l in open("pre.md", encoding="utf-8") if (m := H.match(l.rstrip("\r\n")))]
deep = [i for n, i in hs if n > MAX_HASH]
collapse = []
for f in sorted(glob.glob("collapse/C*/decisions.tsv")):
    for ln in open(f, encoding="utf-8").read().splitlines()[1:]:
        c = ln.split("\t")
        if len(c) > 1 and c[1].strip().upper() == "COLLAPSE":
            collapse.append(c[0].strip())
kids = []
for p in collapse:
    pp = p[:-1]                      # "…-0" -> "…-"
    d = len(p.split("-"))
    kids += [i for n, i in hs if i.startswith(pp) and len(i.split("-")) == d + 1 and n <= MAX_HASH]
drop = sorted(set(NONE + deep + kids))
print(f"drop: NONE {len(NONE)}, deeper than {MAX_HASH}#: {len(deep)}, collapsed children {len(kids)} "
      f"(from {len(collapse)} groups) -> {len(drop)}")
subprocess.run([sys.executable, "-X", "utf8", "apply_anchors.py", "pre.md", "parts-final", out_md, report,
                "--drop", ",".join(drop)], check=True)
# rejoin the split ordinal ག|སུམ་པ (end of old ^2-18 / start of old ^2-19), whatever heading sits between
t = open(out_md, encoding="utf-8", newline="").read()
pat = re.compile(r"(ཕྱིར། )ག( \^[\w-]+\n\n(?:#[^\n]*\n\n)?)(སུམ་པ་ནི། མཐོང་ལམ།)")
t, n = pat.subn(r"\1\2ག\3", t)
open(out_md, "w", encoding="utf-8", newline="").write(t)
print("split ག rejoined:", n)
