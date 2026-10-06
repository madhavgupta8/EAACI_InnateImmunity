import csv,re,sys
sys.path.insert(0,'audit/tmp_M1')
from pages import get
def words(s): return re.findall(r'[a-z0-9]+',s.lower())
for r in csv.DictReader(open('ledger/M1.csv',encoding='utf-8')):
    t=get(r['source'],r['page'])
    t=re.sub(r'-\n\s*','',t)  # crude
    tw=set(words(t))
    # also dehyphenate tokens split across columns: add joined pairs
    toks=words(t); tw|={a+b for a,b in zip(toks,toks[1:])}
    qw=words(r['quote'])
    miss=[w for w in qw if w not in tw]
    if miss: print(r['fact_id'],r['page'],miss)
