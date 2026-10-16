"""Opening (user, 2026-10-16): no ^0-x under the title.
  ## ཀླད་ཀྱི་དོན། ^I-0   title line            ^I-1
  ## མཆོད་བརྗོད། ^II-0   homage (…ཕྱག་འཚལ་ལོ། །)  ^II-1
  ## …ཡན་ལག་ལྔ། ^1-0     preamble འདིར་… + དེ་དག་གི་ནང་ནས… as one block ^1-1
usage: opening.py IN_MD OUT_MD
"""
import re, sys
inp, outp = sys.argv[1:3]
L = open(inp, encoding="utf-8", newline="").read().split("\n")
def one(pred):
    k = [i for i, l in enumerate(L) if pred(l)]
    assert len(k) == 1, k
    return k[0]
a = one(lambda l: l.endswith(" ^0-1")); b = one(lambda l: l.endswith(" ^0-2"))
c = one(lambda l: l.startswith("## ") and l.endswith("^1-0")); d = one(lambda l: l.endswith(" ^1-1"))
assert a < b < c < d and not any(L[k].strip() for k in range(b + 1, c)) and not any(L[k].strip() for k in range(c + 1, d))
pre = re.sub(r" \^0-2$", "", L[b])
m = re.search(r"ཕྱག་འཚལ་ལོ།[\s ]*།", pre)
homage, preamble = pre[:m.end()], pre[m.end():]
assert preamble.startswith("འདིར་"), repr(preamble[:20])
new = ["## ཀླད་ཀྱི་དོན། ^I-0", "", re.sub(r" \^0-1$", " ^I-1", L[a]), "",
       "## མཆོད་བརྗོད། ^II-0", "", homage + " ^II-1", "",
       L[c], "", preamble.rstrip(" ") + L[d]]     # preamble keeps its own NBSP; no added space
L = L[:a] + new + L[d + 1:]
open(outp, "w", encoding="utf-8", newline="").write("\n".join(L))
print("opening restructured")
