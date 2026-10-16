"""Body IDs inside the 8 chapters (^2-2-2-2-2-2-N-…) become ^2-N-k (user, 2026-10-16).
Frame blocks under ## ^2-0 before chapter 1 keep ^2-k; the conclusion (^2-3-0) continues that counter.
usage: chapter_ids.py IN_MD OUT_MD OLD_MAP NEW_MAP"""
import re, sys
inp, outp, oldmap, newmap = sys.argv[1:5]
H = re.compile(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$")
L = open(inp, encoding="utf-8", newline="").read().split("\n")
zone, cnt, ren = None, {}, {}
for k, l in enumerate(L):
    m = H.match(l)
    if m:
        s = m.group(3).split("-")
        if len(m.group(1)) == 2: zone = s[0]
        if m.group(3).startswith("2-2-2-2-2-2-") and len(s) == 8: zone = "2-" + s[6]
        if m.group(3) == "2-3-0": zone = "2"
        continue
    b = re.search(r" \^([\w-]+)$", l)
    if b and zone:
        cnt[zone] = cnt.get(zone, 0) + 1
        nid = f"{zone}-{cnt[zone]}"
        ren[b.group(1)] = nid
        L[k] = l[: b.start()] + " ^" + nid
open(outp, "w", encoding="utf-8", newline="").write("\n".join(L))
rows = open(oldmap, encoding="utf-8").read().splitlines()
with open(newmap, "w", encoding="utf-8") as w:
    w.write(rows[0] + "\n")
    for r in rows[1:]:
        o, n = r.split("\t")
        w.write(o + "\t" + ",".join(ren[x] for x in n.split(",") if x) + "\n")
print("renamed", sum(1 for a, b in ren.items() if a != b), "of", len(ren), "| zones:", {z: c for z, c in cnt.items()})
