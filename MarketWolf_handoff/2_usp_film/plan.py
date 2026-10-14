import json, re
V=json.load(open('vo/vo.json'))
def w(k,prefix,n=1,end=False):
    c=0
    for word,a,b in V[k]['words']:
        if re.sub(r'[^a-z0-9]','',word.lower()).startswith(prefix):
            c+=1
            if c==n: return b if end else a
    raise KeyError((k,prefix,n))
pre={'l1':.7}; post={'l3':1.9,'l8':2.8}
S=[]; VO={}; t=0.0
for i in range(1,9):
    k=f'l{i}'; S.append(round(t,2)); v=t+pre.get(k,.35); VO[k]=round(v,3)
    t=v+V[k]['dur']+post.get(k,.6)
END=round(t,2)
C=lambda k,p,n=1,end=False: round(VO[k]+w(k,p,n,end),3)
CUE={
 'l1_every':C('l1','every'),'l1_very':C('l1','very'),
 'l2_most':C('l2','most'),'l2_entry':C('l2','entry'),'l2_exit':C('l2','exit'),
 'l3_exit':C('l3','exit'),'l3_enter':C('l3','enter'),'l3_target':C('l3','target'),'l3_stop':C('l3','stop'),'l3_end':round(VO['l3']+V['l3']['dur'],3),
 'l4_trade':C('l4','trade'),'l4_analysts':C('l4','analysts'),'l4_each':C('l4','each'),'l4_already':C('l4','already'),
 'l5_indices':C('l5','indices'),'l5_stocks':C('l5','stocks'),'l5_commod':C('l5','commodities'),'l5_one':C('l5','one'),'l5_gold':C('l5','gold'),'l5_crude':C('l5','crude'),'l5_eleven':C('l5','eleven'),
 'l6_nineteen':C('l6','nineteen'),'l6_zero':C('l6','zero'),'l6_nothing':C('l6','nothing'),
 'l7_only':C('l7','only'),'l7_registered':C('l7','registered'),'l7_support':C('l7','support'),
 'l8_mw':C('l8','marketwolf'),'l8_trade':C('l8','trade'),
}
json.dump({'S':S,'END':END,'VO':VO,'CUE':CUE},open('timeline.json','w'),indent=1)
open('film/timing.js','w').write('window.TL='+json.dumps({'S':S,'END':END,'CUE':CUE})+';')
print('scenes',S,'END',END)
for k,v in CUE.items(): print(f'  {k:14s}{v:7.2f}')
