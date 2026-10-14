import json, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
SR=44100; T=json.load(open('timeline.json')); END=T['END']; Q=T['CUE']; S=T['S']
N=int(END*SR)+SR; rng=np.random.default_rng(5)
def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def sos(kind, f, order=2):
    f = [min(max(x, 20), SR / 2 - 200) for x in f] if isinstance(f, (list, tuple)) else min(max(f, 20), SR / 2 - 200)
    return butter(order, f, btype=kind, fs=SR, output='sos')
def filt(x, kind, f, order=2): return sosfilt(sos(kind, f, order), x)
def place(buf, sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= buf.shape[1]: return
    if i < 0: sig = sig[-i:]; i = 0
    sig = sig[:buf.shape[1] - i]
    buf[0, i:i + len(sig)] += sig * gain * np.cos((pan + 1) * np.pi / 4) * 1.414
    buf[1, i:i + len(sig)] += sig * gain * np.sin((pan + 1) * np.pi / 4) * 1.414
def room(st, wet=.18, dur=2.4):
    n = int(dur * SR); ir = rng.standard_normal((2, n)) * np.exp(-np.arange(n) / (dur / 6 * SR))
    ir = np.vstack([filt(ir[0], 'lowpass', 4000), filt(ir[1], 'lowpass', 4000)]) * .05
    return st + wet * np.vstack([fftconvolve(st[0], ir[0])[:st.shape[1]], fftconvolve(st[1], ir[1])[:st.shape[1]]])

# ---------- instruments ----------
def rhodes(m, dur=2.2, vel=1.0):
    n = int(dur * SR); t = np.arange(n) / SR; f = mtof(m)
    idx = 1.6 * vel * np.exp(-t / .35) + .25
    mod = np.sin(2 * np.pi * f * t)
    body = np.sin(2 * np.pi * f * t + idx * mod)
    tine = np.sin(2 * np.pi * f * 14 * t) * np.exp(-t / .015) * .08 * vel
    trem = 1 + .06 * np.sin(2 * np.pi * 4.2 * t)
    env = np.exp(-t / 1.1) * np.minimum(1, t / .004)
    rel = int(.25 * SR); env[-rel:] *= np.linspace(1, 0, rel)
    return (body + tine) * env * trem * vel
def chord_hit(notes, dur, vel):
    out = np.zeros(int(dur * SR))
    for j, m in enumerate(notes):
        x = rhodes(m, dur, vel * (.9 if j else 1.0)); s = int(j * .008 * SR)  # tiny strum
        out[s:s + len(x)] += x[:len(out) - s]
    return out / len(notes) * 1.6
def pad(notes, dur):
    n = int(dur * SR); t = np.arange(n) / SR; L = np.zeros(n); R = np.zeros(n)
    for m in notes:
        for det, p in ((-.06, -.8), (.06, .8)):
            ph = 2 * np.pi * mtof(m + det) * t + rng.random() * 6
            x = np.sin(ph) + .3 * np.sin(2 * ph) + .12 * np.sin(3 * ph)
            L += x * np.cos((p + 1) * np.pi / 4); R += x * np.sin((p + 1) * np.pi / 4)
    a = min(n, int(1.2 * SR)); r = min(n, int(1.2 * SR))
    e = np.ones(n); e[:a] = np.linspace(0, 1, a) ** 2; e[-r:] *= np.linspace(1, 0, r) ** 2
    k = e / (len(notes) * 2)
    return np.vstack([filt(L * k, 'lowpass', 1300), filt(R * k, 'lowpass', 1300)])
def sub(m, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * mtof(m) * t) + .15 * np.sin(4 * np.pi * mtof(m) * t)
    e = np.minimum(1, t / .03) * np.exp(-t / 2.5); r = int(.3 * SR); e[-r:] *= np.linspace(1, 0, r)
    return x * e
def soft_kick():
    n = int(.35 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(50 + 40 * np.exp(-t / .03)) / SR) * np.exp(-t / .14)
def brush(dur=.09):
    n = int(dur * SR); t = np.arange(n) / SR
    return filt(rng.standard_normal(n), 'bandpass', [3000, 9000]) * np.minimum(1, t / .01) * np.exp(-t / .03)
def bell(m, dur=3.0):
    n = int(dur * SR); t = np.arange(n) / SR; f = mtof(m)
    x = np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t / .6) + .12 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t / .3)
    return x * np.exp(-t / 1.2) * np.minimum(1, t / .003)


CH=[[57,61,64,66],[54,57,61,62],[54,57,59,62],[55,59,62,64]]; BASS=[38,35,31,33]
music=np.zeros((2,N)); perc=np.zeros((2,N)); BAR=2.0
p=pad([50]+CH[0],S[1]+1.0); music[:,:p.shape[1]]+=p*.8
t,bar=S[1]-.2,0
while t<S[7]+.4:
    ci=bar%4
    place(music,chord_hit(CH[ci],2.2,.72),t,.5,-.15); place(music,chord_hit(CH[ci][1:],1.0,.42),t+1.25,.33,.2)
    place(music,sub(BASS[ci],2.0),t,.55)
    pp=pad(CH[ci],2.4); place(music,pp[0],t,.33,-.6); place(music,pp[1],t,.33,.6)
    if bar>=2:
        place(perc,soft_kick(),t,.3)
        for e in range(8): place(perc,brush(),t+e*.25,.07+.04*(e%2),.35 if e%2 else -.35)
    if bar%4==3: place(music,rhodes(CH[ci][-1]+12,1.5,.4),t+1.5,.12,.4)
    t+=BAR; bar+=1
fin=S[7]+.4; po=pad([50]+CH[0],END-fin+.5)
place(music,po[0],fin,.85,-.3); place(music,po[1],fin,.85,.3)
place(music,chord_hit(CH[0]+[69],4.0,.6),Q['l8_mw'],.5)
place(music,bell(81,4.0),Q['l8_mw']+.05,.08,-.2); place(music,bell(86,4.0),Q['l8_mw']+.2,.05,.25)
music=room(music+perc*.9,.2)
sfx=np.zeros((2,N))
def tap(soft=1.0):
    n = int(.025 * SR); t = np.arange(n) / SR
    x = filt(rng.standard_normal(n), 'bandpass', [2500, 6000]) * np.exp(-t / .0025) * .5
    x += np.sin(2 * np.pi * 140 * t) * np.exp(-t / .006) * .4
    return x * soft
def tock():
    n = int(.12 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(230 + 60 * np.exp(-t / .01)) / SR) * np.exp(-t / .03) * .6 + tap(.6)[:n] if False else \
        np.pad(tap(.6), (0, n - int(.025 * SR))) + np.sin(2 * np.pi * np.cumsum(230 + 60 * np.exp(-t / .01)) / SR) * np.exp(-t / .03) * .6
def swish(dur=.55):
    n = int(dur * SR); x = rng.standard_normal(n); y = np.zeros(n); blk = 256
    for b in range(0, n, blk):
        p = b / n; f = 300 * (1600 / 300) ** np.sin(np.pi * p)
        y[b:b + blk] = sosfilt(sos('bandpass', [f * .6, f * 1.5]), x[b:b + blk])
    tt = np.linspace(0, 1, n); return y * np.sin(np.pi * tt) ** 2

def tick(f=2200):
    n=int(.05*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*f*tt)*np.exp(-tt/.008)*.5+tap(.5)[:n] if False else np.pad(tap(.5),(0,n-len(tap(.5))))+np.sin(2*np.pi*f*tt)*np.exp(-tt/.008)*.35
place(sfx,swish(.9),.15,.08,-.3)                     # line draws
for k in ['l1_every','l1_very']: place(sfx,tick(1800),Q[k]-.1,.12)
place(sfx,swish(.7),S[1]+.2,.06,.2)
place(sfx,tick(1500),Q['l2_entry'],.12); place(sfx,tick(1100),Q['l2_exit'],.12)
place(sfx,tick(2000),Q['l3_exit']+.5,.14,-.2); place(sfx,tick(2400),Q['l3_target'],.12,.2); place(sfx,tick(1600),Q['l3_stop'],.12,-.2)
place(sfx,tock(),Q['l3_enter']+.55,.28)
place(sfx,bell(88,1.5),Q['l3_end']+1.12,.1,.2)        # exit at target
place(sfx,swish(.8),S[3]-.15,.08,.2)
for k in ['l4_analysts','l4_each']: place(sfx,tap(),Q[k],.16)
place(sfx,swish(.8),S[4]-.3,.08,-.2)
for tt_ in [Q['l5_indices'],Q['l5_commod']+.25,Q['l5_gold']-1.0]: place(sfx,tick(1900),tt_,.1)
for k in ['l5_gold','l5_crude']: place(sfx,tick(2600),Q[k]+.05,.12)
place(sfx,tap(.7),Q['l5_eleven'],.14)
pass
[place(sfx,tick(2000+200*i),Q['l6_zero']+i*.12,.1) for i in range(3)]; place(sfx,tick(1800),Q['l6_nothing'],.1)
for k in ['l7_only','l7_registered','l7_support']: place(sfx,tap(),Q[k],.16)
place(sfx,swish(.8),S[7]-.25,.08)
vo=np.zeros((2,N)); iv=[]
for k,st in T['VO'].items():
    sr,x=wavfile.read(f'vo/{k}.wav'); x=x.astype(np.float64)/32768; x=filt(x,'highpass',75); x/=np.max(np.abs(x))+1e-9
    x=np.tanh(x*1.25)/np.tanh(1.25); i=int(st*SR); m=min(len(x),N-i); vo[0,i:i+m]+=x[:m]; vo[1,i:i+m]+=x[:m]; iv.append((st,st+len(x)/SR))
vo=room(vo,.05,1.0)
duck=np.ones(N); tt=np.arange(N)/SR
for a,b in iv:
    g=np.clip(np.minimum((tt-(a-.25))/.25,((b+.5)-tt)/.5),0,1); duck=np.minimum(duck,1-.7*g)
mix=music*duck*.27+sfx+vo*.9
e=int(END*SR); fo=int(1.0*SR); mix[:,e-fo:e]*=np.linspace(1,0,fo)**1.5; mix=mix[:,:e]; mix/=np.max(np.abs(mix))*1.05
wavfile.write('mix2_raw.wav',SR,(mix.T*32767).astype(np.int16)); print('ok',END)
