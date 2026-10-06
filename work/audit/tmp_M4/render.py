import re,subprocess
h=open('/Users/madhavgupta/Projects/Papa_EAACIexam/pack/modules/M4-phagocytosis.html',encoding='utf-8').read()
figs=re.findall(r'<figure class="diagram" id="(D\d+)">(.*?)</figure>',h,re.S)
for fid,body in figs:
    vb=re.search(r'viewBox="0 0 (\d+) (\d+)"',body)
    H=int(vb.group(2))
    p=f'/Users/madhavgupta/Projects/Papa_EAACIexam/work/audit/tmp_M4/{fid}.html'
    open(p,'w').write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" href="/Users/madhavgupta/Projects/Papa_EAACIexam/pack/assets/style.css"><style>body{{margin:0}} main{{max-width:none;padding:0}} figure{{margin:0;width:800px}}</style></head><body><main><figure class="diagram">{body}</figure></main></body></html>')
    subprocess.run(['/Users/madhavgupta/Library/Caches/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-mac-arm64/chrome-headless-shell','--headless','--hide-scrollbars',f'--screenshot=/Users/madhavgupta/Projects/Papa_EAACIexam/work/audit/png_M4/{fid}.png','--window-size=820,%d'%(H+120),'file://'+p],capture_output=True)
    print(fid,H)
