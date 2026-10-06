import re,glob,csv,sys
pages={}
for f in glob.glob('sources_text/*.txt'):
    src='Abbas' if 'abbas' in f else 'Janeway' if 'janeway' in f else 'HAE-GL' if 'hae' in f else None
    if not src: continue
    cur=None
    for line in open(f,encoding='utf-8'):
        m=re.match(r'##### \[(?:Abbas 11e|Janeway[^\]]*?|[^\]]*?) p\.(\S+?)\]',line)
        if m: cur=(src,m.group(1)); pages.setdefault(cur,''); continue
        if cur: pages[cur]+=line
def norm(s): return re.sub(r'[^a-z0-9]','',s.lower())
def get(src,page):
    out=''
    for p in str(page).split('-'):
        out+=pages.get((src,p),'')
    return out
if __name__=='__main__':
    for r in csv.DictReader(open('ledger/M1.csv',encoding='utf-8')):
        t=get(r['source'],r['page'])
        q=norm(r['quote'].replace('...',''))
        ok = all(norm(part) in norm(t) for part in r['quote'].split('...'))
        if not ok: print('QUOTE MISMATCH',r['fact_id'],r['source'],r['page'],'|',r['quote'][:80], 'pagefound' if t else 'NOPAGE')
