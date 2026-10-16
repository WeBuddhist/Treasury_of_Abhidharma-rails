"""རྒྱ་མཚོའི་སྙིང་པོ། opening (title line -> ^I, homage + commitment verses -> ^II; no preface) + chapter body IDs ^1-N-k.
Opening blocks under the # title (^0-1 … ^0-10) become:
  ## ཀླད་ཀྱི་དོན། ^I-0        title lines (2)
  ## མཆོད་བརྗོད། ^II-0         homage + verses of commitment (4)
  ## སྔོན་བྱུང་། ^III-0        prose preface incl. the 'three parts' sentence (4)
Body IDs: inside chapter N (heading ^2-2-3-2-N-0) -> ^2-N-k; other blocks keep a counter per ## label.
usage: opening_chapters.py IN_MD OUT_MD OLD_MAP NEW_MAP
"""
import re, sys
inp, outp, oldmap, newmap = sys.argv[1:5]
H = re.compile(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$")
raw = open(inp, encoding="utf-8", newline="").read()
fm = re.match(r"\A---\n.*?\n---\n", raw, flags=re.S)
head, body = raw[:fm.end()], raw[fm.end():]
units = body.strip("\n").split("\n\n")
t = next(i for i, u in enumerate(units) if u.startswith("# "))
c1 = next(i for i, u in enumerate(units) if (m := H.match(u)) and m.group(3) == "1-0")
op = units[t + 1:c1]
assert len(op) == 10, len(op)
strip = lambda u: re.sub(r"^[​\s༄༅།]*", "", u)
assert strip(op[0]).startswith("ཆོས་མངོན་པའི་མཛོད་ཀྱི་རྣམ་པར་བཤད་པ"), op[0][:30]
assert strip(op[1]).startswith("དཔལ་དང་ལྡན་པའི་ཞིང་ཁམས"), op[1][:30]
new_op = ["## ཀླད་ཀྱི་དོན། ^I-0"] + op[0:1] + ["## མཆོད་བརྗོད། ^II-0"] + op[1:10]
units = units[:t + 1] + new_op + units[c1:]
IDT = re.compile(r" \^[\w-]+$")
zone, cnt, out, ren = None, {}, [], {}
for u in units:
    m = H.match(u)
    if m:
        s = m.group(3).split("-")
        if len(m.group(1)) == 1: zone = "0"
        elif len(m.group(1)) == 2: zone = s[0]
        if m.group(3).startswith("1-2-3-4-2-2-") and len(s) == 8: zone = "1-" + s[6]
        out.append(u); continue
    old = re.search(r"\^([\w-]+)$", u).group(1)
    cnt[zone] = cnt.get(zone, 0) + 1
    nid = f"{zone}-{cnt[zone]}"
    ren[old] = nid
    out.append(IDT.sub("", u) + " ^" + nid)
open(outp, "w", encoding="utf-8", newline="").write(head + "\n" + "\n\n".join(out) + "\n")
rows = open(oldmap, encoding="utf-8").read().splitlines()
with open(newmap, "w", encoding="utf-8") as w:
    w.write(rows[0] + "\n")
    for r in rows[1:]:
        o, n = r.split("\t")
        w.write(o + "\t" + ",".join(ren[x] for x in n.split(",") if x) + "\n")
print({z: c for z, c in cnt.items()})
