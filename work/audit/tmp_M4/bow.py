import csv,re,sys
sys.path.insert(0,'audit/tmp_M4')
from pages import pages,norm
def toks(s): return set(w for w in norm(s).split() if len(w)>3)
for r in csv.DictReader(open('ledger/M4.csv',encoding='utf-8')):
    pg=r['page'].split('-'); pl=pg if len(pg)==1 else [str(x) for x in range(int(pg[0]),int(pg[1])+1)]
    txt=' '.join(pages.get((r['source'],p),'') for p in pl)
    # merge hyphen line breaks crudely: add concatenations of fragments
    pt=toks(txt)
    frags=re.findall(r'(\w+)-\s',txt)
    q=toks(r['quote'])
    miss=[w for w in q if w not in pt and not any(w.startswith(f.lower()) for f in frags if len(f)>2)]
    score=1-len(miss)/max(1,len(q))
    best=max(((sum(1 for w in q if w in toks(v))/max(1,len(q))),k) for k,v in pages.items())
    if score<0.95: print(r['fact_id'],r['page'],round(score,2),miss,'best',best)
