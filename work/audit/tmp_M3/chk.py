import csv,re,glob,sys
pages={}
for f in glob.glob('sources_text/*.txt'):
    cur=None
    for line in open(f,encoding='utf-8',errors='replace'):
        m=re.match(r'##### \[(Abbas|Janeway) \d+e p\.(\d+)\]',line)
        if m: cur=(m.group(1),m.group(2)); pages.setdefault(cur,''); continue
        m=re.match(r'##### \[HAE.*?p\.(\d+)\]',line)
        if m: cur=('HAE-GL',m.group(1)); pages.setdefault(cur,''); continue
        if cur: pages[cur]+=line
def norm(s): return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
def text(src,pg):
    ps=pg.split('-')
    if len(ps)==2: return ' '.join(pages.get((src,str(p)),'') for p in range(int(ps[0]),int(ps[1])+1))
    return pages.get((src,pg),'')
if __name__=='__main__':
    for r in csv.DictReader(open('ledger/M3.csv')):
        t=norm(text(r['source'],r['page'])); q=norm(r['quote'])
        ok=q in t
        if not ok:
            # find which page has it
            found=[k for k,v in pages.items() if q in norm(v)]
            print(r['fact_id'],'NOTFOUND',r['source'],r['page'],'found at',found[:3],'|',r['quote'][:80])

def decol(t):
    L=[];R=[]
    for line in t.split('\n'):
        s=line.strip()
        parts=re.split(r'\s{3,}',s)
        if len(parts)>=2: L.append(parts[0]); R.append(' '.join(parts[1:]))
        else: L.append(s)
    out=' '.join(L)+' '+' '.join(R)
    return re.sub(r'-\s+([a-z])',r'\1',out)
def score(src,pg,q):
    t=norm(decol(text(src,pg))); qn=norm(re.sub(r'-\s+([a-z])',r'\1',q))
    if qn in t: return 1.0
    tw=set(t.split()); qw=qn.split()
    return sum(w in tw for w in qw)/max(1,len(qw))
