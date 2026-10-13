import re
exec(open('survey.py').read().split('import collections')[0])
def syl(l):
    t=re.sub(r'[​\xa0 ]','',l)
    t=re.sub(r'[།༄༅]+','་',t)
    return len([s for s in t.split('་') if s])
ch=0; counts={}
for b in blocks:
    first=lines[b[0]-1]
    if first.startswith('## '):
        ch+=1; continue
    n=b[1]-b[0]+1
    s=[syl(lines[k-1]) for k in range(b[0],b[1]+1)]
    counts.setdefault(ch,0); counts[ch]+=1
    if len(set(s))>1 or n!=4: print(ch,b,n,s)
print(counts)
