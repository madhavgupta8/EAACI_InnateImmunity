import re,glob,csv,sys,unicodedata
pages={}
for f in glob.glob('/Users/madhavgupta/Projects/Papa_EAACIexam/work/sources_text/*.txt'):
    src=None
    if 'abbas' in f: src='Abbas'
    elif 'janeway' in f: src='Janeway'
    elif 'hae' in f: src='HAE-GL'
    else: continue
    cur=None
    for line in open(f,encoding='utf-8'):
        m=re.match(r'##### \[\S+ \S+ p\.(\d+)\]',line)
        if m: cur=(src,int(m.group(1))); pages[cur]=''; continue
        if cur: pages[cur]+=line
def norm(s):
    s=unicodedata.normalize('NFKC',s).lower()
    s=s.replace('–','-').replace('—','-').replace('’',"'").replace('“','"').replace('”','"')
    s=re.sub(r'-\s*\n\s*','',s)
    s=re.sub(r'[^a-z0-9αβγδεκ%<>]+',' ',s)
    return ' '.join(s.split())
def get(src,page):
    ps=[int(x) for x in str(page).split('-')]
    rng=range(ps[0],ps[-1]+1)
    return '\n'.join(pages.get((src,p),'') for p in rng)

def cols(txt):
    L=[];R=[]
    for line in txt.split('\n'):
        parts=re.split(r' {3,}',line.strip(),maxsplit=1)
        L.append(parts[0]); R.append(parts[1] if len(parts)>1 else '')
    return '\n'.join(L)+'\n'+'\n'.join(R)
def alltext(src,page):
    raw=get(src,page)
    return norm(raw)+' || '+norm(cols(raw))
