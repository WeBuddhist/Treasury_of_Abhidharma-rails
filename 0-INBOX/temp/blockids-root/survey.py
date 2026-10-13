import re,sys
INVIS=set('​‌‍﻿⁠ \t\xa0\r')
def is_sep(l): return all(c in INVIS for c in l)
lines=open('original.md',encoding='utf-8').read().split('\n')
# skip frontmatter
start=lines.index('---',1)+1
blocks=[];cur=None
for i in range(start,len(lines)):
    l=lines[i]
    if is_sep(l):
        if cur: blocks.append(cur);cur=None
    else:
        if cur is None: cur=[i+1,i+1]
        else: cur[1]=i+1
if cur: blocks.append(cur)
import collections
c=collections.Counter(b[1]-b[0]+1 for b in blocks)
print(len(blocks),c)
for b in blocks:
    n=b[1]-b[0]+1
    first=lines[b[0]-1]
    if n!=4 or first.startswith('#') or any(len(lines[k-1])>60 for k in range(b[0],b[1]+1)):
        print(b, n, first[:70].replace('\xa0','_').replace('​',''))
