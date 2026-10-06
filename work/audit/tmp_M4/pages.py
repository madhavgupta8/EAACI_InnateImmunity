import re,glob,csv,sys
pages={}
for f in glob.glob('sources_text/*.txt'):
    src='Abbas' if 'abbas' in f else 'Janeway' if 'janeway' in f else 'HAE-GL' if 'hae' in f else None
    if not src: continue
    txt=open(f,encoding='utf-8').read()
    parts=re.split(r'(##### \[[^\]]*p\.(\d+)\][^\n]*#####)',txt)
    for i in range(1,len(parts),3):
        pages.setdefault((src,parts[i+1]),'')
        pages[(src,parts[i+1])]+=parts[i+2]
def norm(s): return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
if __name__=='__main__':
    for r in csv.DictReader(open('ledger/M4.csv',encoding='utf-8')):
        pg=r['page'].split('-')
        txt=''.join(pages.get((r['source'],p),'') for p in (pg if len(pg)==1 else [str(x) for x in range(int(pg[0]),int(pg[1])+1)]))
        segs=[s for s in re.split(r'\.\.\.|…',r['quote']) if s.strip()]
        ok=all(norm(s) in norm(txt) for s in segs)
        if not ok:
            # find which page contains
            found=[k for k,v in pages.items() if all(norm(s) in norm(v) for s in segs)]
            print(r['fact_id'],'NOTFOUND on',r['page'],'found:',found)
