import re,csv,sys
sys.path.insert(0,'audit/tmp_M5')
from pages import pages
def words(s): return [w for w in re.findall(r'[a-z0-9]+',s.lower().replace('-',' ')) if len(w)>2]
for r in csv.DictReader(open('ledger/M5.csv',encoding='utf-8')):
    src=r['source']; pg=r['page']
    pgs=pg.split('-')
    if len(pgs)==2: pgs=[str(p) for p in range(int(pgs[0]),int(pgs[1])+1)]
    t=set(words(''.join(pages.get((src,p),'') for p in pgs)))
    qw=words(r['quote'])
    miss=[w for w in qw if w not in t]
    if not t: print(r['fact_id'],'PAGE MISSING',src,pg)
    elif len(miss)>0: 
        # where would it fit
        best=max(((k,sum(w in set(words(v)) for w in qw)) for k,v in pages.items() if k[0]==src),key=lambda x:x[1])
        print(r['fact_id'],pg,'missing',miss,'best',best,len(qw))
