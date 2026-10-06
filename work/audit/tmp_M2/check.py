import sys; sys.path.insert(0,'/Users/madhavgupta/Projects/Papa_EAACIexam/work/audit/tmp_M2')
from pages import *
for r in csv.DictReader(open('/Users/madhavgupta/Projects/Papa_EAACIexam/work/ledger/M2.csv',encoding='utf-8')):
    t=alltext(r['source'],r['page'])
    frags=[norm(x) for x in re.split(r'\.\.\.|…',r['quote']) if norm(x)]
    bad=[x for x in frags if x not in t]
    if bad:
        # word coverage
        ws=set(t.split()); cov=[sum(w in ws for w in b.split())/len(b.split()) for b in bad]
        print(r['fact_id'],r['page'],'MISSING:',bad, ['%.2f'%c for c in cov])
