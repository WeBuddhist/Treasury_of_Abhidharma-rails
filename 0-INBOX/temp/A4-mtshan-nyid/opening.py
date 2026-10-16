"""མཚན་ཉིད་རྗེས་འབྲང་ opening (user, 2026-10-16): ^1-1 (Sanskrit/Tibetan title + translator's homage) -> ## ཀླད་ཀྱི་དོན། ^I-0 / ^I-1;
^1-2, ^1-3 (Pūrṇavardhana's homage + commitment verses) -> ## མཆོད་བརྗོད། ^II-0 / ^II-1, ^II-2; chapter 1 blocks renumbered from ^1-1.
usage: opening.py IN OUT MAP"""
import re, sys
inp, outp, mapp = sys.argv[1:4]
H = re.compile(r"^(#+)\s+(.*?)\s*\^([\w-]+)\s*$")
raw = open(inp, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in raw else "\n"
raw = raw.replace("\r\n", "\n")
fm = re.match(r"\A---\n.*?\n---\n", raw, flags=re.S)
head, body = raw[:fm.end()], raw[fm.end():]
units = [u for u in body.strip("\n").split("\n\n") if u.strip()]   # skips the one double blank line
c1 = next(i for i, u in enumerate(units) if (m := H.match(u)) and m.group(3) == "1-0")
op = units[c1 + 1:c1 + 4]
assert [re.search(r"\^([\w-]+)$", u).group(1) for u in op] == ["1-1", "1-2", "1-3"], op
assert "རྒྱ་གར་སྐད་དུ" in op[0] and op[0].rstrip().endswith("^1-1")
assert re.search(r"\^1-4$", units[c1 + 4]) and "བསྟན་བཅོས་མཛད་པར་བཞེད་པས" in units[c1 + 4][:40]
units = units[:c1] + ["## ཀླད་ཀྱི་དོན། ^I-0", op[0], "## མཆོད་བརྗོད། ^II-0", op[1], op[2]] + [units[c1]] + units[c1 + 4:]
IDT = re.compile(r" \^[\w-]+$")
zone, cnt, out, ren = None, {}, [], {}
for u in units:
    m = H.match(u)
    if m:
        zone = "0" if len(m.group(1)) == 1 else m.group(3).split("-")[0] if len(m.group(1)) == 2 else zone
        out.append(u); continue
    old = re.search(r"\^([\w-]+)$", u).group(1)
    cnt[zone] = cnt.get(zone, 0) + 1
    nid = f"{zone}-{cnt[zone]}"; ren[old] = nid
    out.append(IDT.sub("", u) + " ^" + nid)
open(outp, "w", encoding="utf-8", newline="").write((head + "\n" + "\n\n".join(out) + "\n").replace("\n", nl))
open(mapp, "w", encoding="utf-8").write("old_id\tnew_id\n" + "".join(f"{o}\t{n}\n" for o, n in ren.items()))
print({z: c for z, c in cnt.items()}, "renamed", sum(1 for o, n in ren.items() if o != n))
