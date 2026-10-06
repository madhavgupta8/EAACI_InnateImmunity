import csv
p='ledger/M1.csv'
rows=list(csv.DictReader(open(p,encoding='utf-8')))
F=list(rows[0].keys())
d={r['fact_id']:r for r in rows}
d['M1-F039'].update(fact='Lysozyme (a glycosidase) and secretory phospholipase A2 are secreted in tears and saliva and by phagocytes; Paneth cells also make both.',
  quote='secreted in tears and saliva and by phagocytes. Lysozyme is a glycosidase ... Lysozyme is also produced by Paneth cells')
d['M1-F083'].update(fact='Neutrophils arrive first because they are the most abundant leukocytes and the most rapid responders; monocytes become more numerous over time and may dominate some reactions because they live longer and can proliferate locally.',
  quote='may be the dominant population in some reactions because they have longer lifespans than neutrophils and are capable of local proliferation')
d['M1-F086'].update(fact='TNF, IL-1 and IL-6 are three of the most important proinflammatory cytokines of innate immunity; innate cytokines are made mainly by tissue macrophages and DCs.', page='90-91')
d['M1-F091'].update(fact='Endogenous pyrogens (TNF-alpha, IL-1beta, IL-6) induce cyclooxygenase-2 and prostaglandin E2; PGE2 acts on the hypothalamus to increase heat production and vasoconstriction.')
new=[('M1-F125','Antagonists of TNF, IL-1, IL-6 and IL-12 or their receptors are used to reduce inflammation in rheumatoid arthritis, inflammatory bowel disease and psoriasis.','Abbas','97','Antagonists against all of these cytokines or their receptors are used clinically to reduce inflammation'),
 ('M1-F126','In the airways, goblet cells secrete mucus, and beating cilia move the mucus outward to trap and eject pathogens.','Janeway','48','Beating of the cilia moves a continuous stream of mucus secreted by goblet cells (green) outward, trapping and ejecting potential pathogens'),
 ('M1-F127','The pentraxins include the short pentraxins CRP and SAP and the long pentraxin PTX3.','Abbas','87','include the short pentraxins, C-reactive protein (CRP) and serum amyloid P (SAP), and the long pentraxin PTX3')]
for fid,fact,s,pg,q in new:
    rows.append(dict(fact_id=fid,module='M1',fact=fact,source=s,page=pg,quote=q,volatile='N',verified_by=''))
w=csv.DictWriter(open(p,'w',newline='',encoding='utf-8'),F,quoting=csv.QUOTE_MINIMAL)
w.writeheader(); w.writerows(rows)
