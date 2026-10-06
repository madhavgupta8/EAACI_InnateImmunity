import re,glob,csv,sys
pages={}
for f in glob.glob('sources_text/*.txt'):
    txt=open(f,encoding='utf-8').read()
    parts=re.split(r'^##### \[(\w+)[^\]]*? p\.(\S+?)\][^\n]*#####$',txt,flags=re.M)
    for i in range(1,len(parts),3):
        pages[(parts[i],parts[i+1])]=pages.get((parts[i],parts[i+1]),'')+parts[i+2]
def norm(s): return re.sub(r'[^a-z0-9]','',s.lower().replace('–','-'))
if __name__=='__main__':
    for r in csv.DictReader(open('ledger/M5.csv',encoding='utf-8')):
        src=r['source']; pg=r['page']
        pgs=pg.split('-') if '-' in pg else [pg]
        if len(pgs)==2: pgs=[str(p) for p in range(int(pgs[0]),int(pgs[1])+1)]
        t=''.join(pages.get((src,p),'') for p in pgs)
        q=norm(r['quote'])
        if q in norm(t): continue
        found=[k for k,v in pages.items() if k[0]==src and q in norm(v)]
        print(r['fact_id'],pg,'NOT FOUND on page; found on',found)
