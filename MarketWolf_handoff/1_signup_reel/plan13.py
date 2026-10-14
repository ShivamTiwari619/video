import json, math, re
V=json.load(open('audio/v13/v/vo.json'))
ch=lambda x: math.ceil(x*2-1e-9)/2
def w(k,prefix,n=1,end=False):
    c=0
    for word,a,b in V[k]['words']:
        if re.sub(r'[^a-z0-9]','',word.lower()).startswith(prefix):
            c+=1
            if c==n: return b if end else a
    raise KeyError((k,prefix,n))
d=lambda k:V[k]['dur']
VS=.4; GAP=.55
SHIFT=max(0,ch(.35+d('intro')+.3-4.2)); STEP0=4.2+SHIFT
CFG={'SHIFT':SHIFT,'CALM':0}; DUR=[]; cam=[]   # cam keys relative to step: (k, t_rel, sy, z, dur)
# s1
CFG['TYPE1']=round(VS+w('s1','mobile')+.3,2); te=CFG['TYPE1']+9*.11
tap=max(VS+d('s1')+GAP, te+1.1); DUR.append(ch(tap+.55))
cam+= [(1,.5,605,.93,1.1,150,[30,552,576,104,12]),(1,tap-1.2,888,.91,1.0,95,[34,845,568,90,10])]
# s2
o0=VS+w('s2','otp',end=True)+.15; CFG['OTP']=[round(o0+i*.22,2) for i in range(4)]
tap=max(VS+d('s2')+GAP, CFG['OTP'][-1]+1.1); DUR.append(ch(tap+.55))
cam+= [(2,.5,558,.94,1.1,105,[26,506,584,104,12]),(2,tap-1.2,874,.91,1.0,95,[34,831,568,90,10])]
# s3
p0=VS+w('s3','pin',end=True)+.15; CFG['PIN3']=[round(p0+i*.24,2) for i in range(4)]
tap=max(VS+d('s3')+GAP, CFG['PIN3'][-1]+1.0); DUR.append(ch(tap+.55))
cam+= [(3,.5,336,.94,1.1,105,[26,284,584,104,12]),(3,tap-1.2,868,.91,1.0,95,[34,825,568,90,10])]
# s4
p0=VS+w('s4','confirm'); CFG['PIN4']=[round(p0+i*.22,2) for i in range(4)]
tap=max(VS+d('s4')+GAP, CFG['PIN4'][-1]+1.0); DUR.append(ch(tap+.55))
cam+= [(4,.45,336,.94,1.0,105,[26,284,584,104,12]),(4,tap-1.1,868,.91,.9,95,[34,825,568,90,10])]
# s5
a=VS; n1=a+w('s5','no',1); n2=a+w('s5','no',2)
CFG['CARDS']=[round(n1-.05,2),round((n1+n2)/2,2),round(n2-.05,2)]
CFG['ROW']=round(a+w('s5','calls')-.05,2); CFG['CHING']=[round(a+w('s5','ninety'),2),round(a+w('s5','ninety')+.6,2)]
tap=VS+d('s5')+GAP+.2; DUR.append(ch(tap+.55))
cam+= [(5,.3,140,.9,1.0,150,[110,46,420,178,14]),(5,n1-.6,332,.94,1.0,135,[22,232,594,202,14]),(5,CFG['ROW']-.55,1076,.93,1.0,70,[10,1034,616,84,10]),(5,a+w('s5','all')-.45,1225,.92,1.0,80,[30,1178,572,94,10])]
# s6
eng=VS+w('s6','prefer',end=True)+.25; CFG['ENG']=round(eng,2)
tap=max(VS+d('s6')+GAP, eng+1.8); DUR.append(ch(tap+.55))
cam+= [(6,.4,612,.91,1.1,230,[138,430,360,364,182]),(6,VS+w('s6','language')-.6,931,.94,1.0,80,[26,894,584,74,10]),(6,tap-1.25,1112,.91,1.0,95,[30,1066,576,94,10])]
# s7
CFG['KYC']=round(VS+w('s7','complete'),2); CFG['COIN']=round(VS+w('s7','kyc',end=True)+.2,2)
tap=max(VS+d('s7')+GAP, CFG['COIN']+1.1); DUR.append(ch(tap+.55))
cam+= [(7,.4,320,.92,1.1,170,[100,192,436,252,14]),(7,tap-1.25,1170,.91,1.0,95,[34,1126,568,90,10])]
CFG['DUR']=DUR
S=lambda k: STEP0+sum(DUR[:k-1]); T=lambda k: S(k+1)-.2; OUT=S(8)-.2
CAM=[{'t':round(S(k)+tr,3),'sy':sy,'z':z,'d':du,'h':h,'r':r,'k':k} for k,tr,sy,z,du,h,r in cam]
for k in range(1,7): CAM.append({'t':round(T(k)-.4,3),'n':1,'d':.85})
CAM.append({'t':round(OUT-.45,3),'n':1,'d':.75})
CFG['CAM']=sorted(CAM,key=lambda c:c['t'])
o1=.2; o2=max(2.1,o1+d('o1')+.25)
CFG['OUTRO']=ch(o2+d('o2')+2.4)
starts={'intro':.35,'s1':VS,'s2':VS,'s3':VS,'s4':VS,'s5':VS,'s6':VS,'s7':VS,'o1':o1,'o2':o2}
CFG['VO']={'draft_starts':{'v':starts}}
open('reel/timing.js','w').write('window.CFG='+json.dumps(CFG)+';')
print('SHIFT',SHIFT,'DUR',DUR,'total',STEP0+sum(DUR)-.2+CFG['OUTRO'])
