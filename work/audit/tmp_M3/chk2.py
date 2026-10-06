import sys,csv;sys.path.insert(0,'audit/tmp_M3');import chk
for r in csv.DictReader(open('ledger/M3.csv')):
    s=chk.score(r['source'],r['page'],r['quote'])
    if s<1: print(r['fact_id'],r['source'],r['page'],round(s,2),'|',r['quote'][:90])
