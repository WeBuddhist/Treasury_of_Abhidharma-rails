import sys
INVIS=set('​‌‍﻿⁠ \t\xa0\r')
def is_sep(l): return all(c in INVIS for c in l)
src=open('original.md','rb').read()
assert b'\r' not in src
text=src.decode('utf-8')
lines=text.split('\n')
H1='## གནས་དང་པོ་ཁམས་བསྟན་པ། ^1-0'
FIRST='གང་ཞིག་ཀུན་ལ་མུན་པ་གཏན་བཅོམ་ཞིང་'
hi=lines.index(H1); assert lines[hi+1]==''
fi=[i for i,l in enumerate(lines) if l.startswith(FIRST)]; assert len(fi)==1; fi=fi[0]
assert lines[fi-1]==''
# move: remove heading+blank, insert before first stanza
moved=lines[:hi]+lines[hi+2:fi]+[H1,'']+lines[fi:]
assert len(moved)==len(lines)
# blocks
start=moved.index('---',1)+1
blocks=[];cur=None
for i in range(start,len(moved)):
    if is_sep(moved[i]):
        if cur: blocks.append(cur);cur=None
    else:
        if cur is None: cur=[i,i]
        else: cur[1]=i
if cur: blocks.append(cur)
COLO='ཆོས་མངོན་པའི་མཛོད་ཀྱི་ཚིག་ལེའུར་བྱས་པ་ལས།'
ch=0; v=0; colo=0; back=0; after8=False
out=list(moved); ids=[]
for a,b in blocks:
    first=moved[a].lstrip('​')
    if moved[a].startswith('#'):
        assert a==b
        ch=int({'དང་པོ':1,'གཉིས':2,'གསུམ':3,'བཞི':4,'ལྔ':5,'དྲུག':6,'བདུན':7,'བརྒྱད':8}[[k for k in ['དང་པོ','གཉིས','གསུམ','བཞི','ལྔ','དྲུག','བདུན','བརྒྱད'] if moved[a].startswith('## གནས་'+k)][0]])
        assert moved[a].endswith(f'^{ch}-0'),moved[a]
        v=0;colo=0;continue
    if after8:
        id_='^'+'abcdefghij'[back]; back+=1
    elif first.startswith(COLO):
        assert a==b
        id_=f'^{ch}-'+'ab'[colo]; colo+=1
        if ch==8: after8=True
    elif ch==0:
        v+=1; id_=f'^0-{v}'
    else:
        v+=1; id_=f'^{ch}-{v}'
    out[b]=moved[b]+' '+id_
    ids.append((id_,a+1,b+1))
res='\n'.join(out)
# verify
import re
strip=[]
for i,l in enumerate(out):
    if i in {b for _,_,b in [(x,y-1,z-1) for x,y,z in ids]}:
        l=re.sub(r' \^[0-9a-z-]+$','',l)
    strip.append(l)
back_l=strip[:hi]+[H1,'']+strip[hi:fi-2+0]  # placeholder replaced below
# undo move properly
hi2=strip.index(H1)
undone=strip[:hi2]+strip[hi2+2:]
undone=undone[:hi]+[H1,'']+undone[hi:]
assert '\n'.join(undone).encode('utf-8')==src, 'roundtrip failed'
assert len(out)==len(lines)
open(sys.argv[1],'w',encoding='utf-8',newline='\n').write(res)
for t in ids: print(*t)
