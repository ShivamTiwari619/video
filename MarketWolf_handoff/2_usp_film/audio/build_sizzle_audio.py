# Sizzle mix: same lounge palette as Draft 2, quicker harmonic rhythm (1.6s bars), VO from sizzle/vo/.
# Run from 2_usp_film/:  python3 audio/build_sizzle_audio.py  -> sizzle_mix_raw.wav
import json, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile
SR=44100; T=json.load(open('sizzle/timeline.json')); END=T['END']; Q=T['CUE']; S=T['S']
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



def tick(f=2200):
    n = int(.05 * SR); tt = np.arange(n) / SR; tp = tap(.5)
    return np.pad(tp, (0, n - len(tp))) + np.sin(2 * np.pi * f * tt) * np.exp(-tt / .008) * .35
def tap(soft=1.0):
    n = int(.025 * SR); t = np.arange(n) / SR
    x = filt(rng.standard_normal(n), 'bandpass', [2500, 6000]) * np.exp(-t / .0025) * .5
    x += np.sin(2 * np.pi * 140 * t) * np.exp(-t / .006) * .4
    return x * soft
def swish(dur=.45):
    n = int(dur * SR); x = rng.standard_normal(n); y = np.zeros(n); blk = 256
    for b in range(0, n, blk):
        p = b / n; f = 300 * (1600 / 300) ** np.sin(np.pi * p)
        y[b:b + blk] = sosfilt(sos('bandpass', [f * .6, f * 1.5]), x[b:b + blk])
    tt = np.linspace(0, 1, n); return y * np.sin(np.pi * tt) ** 2

CH=[[57,61,64,66],[54,57,61,62],[54,57,59,62],[55,59,62,64]]; BASS=[38,35,31,33]
music=np.zeros((2,N)); perc=np.zeros((2,N)); BAR=1.6
p=pad([50]+CH[0],S[1]+.6); music[:,:p.shape[1]]+=p*.7
t,bar=S[1]-.1,0
while t<S[6]-.1:
    ci=bar%4
    place(music,chord_hit(CH[ci],1.8,.72),t,.5,-.15); place(music,chord_hit(CH[ci][1:],.8,.4),t+1.0,.3,.2)
    place(music,sub(BASS[ci],1.6),t,.55)
    pp=pad(CH[ci],2.0); place(music,pp[0],t,.3,-.6); place(music,pp[1],t,.3,.6)
    place(perc,soft_kick(),t,.28); place(perc,soft_kick(),t+.8,.16)
    for e in range(8): place(perc,brush(),t+e*.2,.06+.035*(e%2),.35 if e%2 else -.35)
    if bar%4==3: place(music,rhodes(CH[ci][-1]+12,1.2,.4),t+1.2,.12,.4)
    t+=BAR; bar+=1
fin=S[6]-.1; po=pad([50]+CH[0],END-fin+.5)
place(music,po[0],fin,.85,-.3); place(music,po[1],fin,.85,.3)
place(music,chord_hit(CH[0]+[69],3.5,.6),Q['end_marketwolf'],.5)
place(music,bell(81,3.0),Q['end_marketwolf']+.05,.08,-.2); place(music,bell(86,3.0),Q['end_marketwolf']+.2,.05,.25)
music=room(music+perc*.9,.2)
sfx=np.zeros((2,N))
place(sfx,tick(1800),Q['hook_in'],.1); place(sfx,swish(.6),Q['hook_very']-.25,.06); place(sfx,tick(2400),Q['hook_out']+.05,.12)
for k in S[1:]: place(sfx,swish(.45),k-.25,.07,.2)
place(sfx,tap(.8),Q['xf_marketwolf'],.14); place(sfx,tick(2000),Q['xf_exit'],.14); place(sfx,tick(1600),Q['xf_enter'],.12)
place(sfx,tick(2400),Q['exit_target'],.12,.2); place(sfx,tick(1600),Q['exit_stop'],.12,-.2); place(sfx,bell(88,1.2),Q['exit_capital']-.05,.08,.2)
for i in range(3): place(sfx,tap(.6),Q['ideas_ideas']-.15+i*.16,.12)
for k in ['app_stocks','app_commodities']: place(sfx,tick(1900),Q[k],.1)
for k in ['price_nineteen','price_zero','price_nothing']: place(sfx,tick(2200),Q[k],.1)
vo=np.zeros((2,N)); iv=[]
for k,st in T['VO'].items():
    sr,x=wavfile.read(f'sizzle/vo/{k}.wav'); x=x.astype(np.float64)/32768; x=filt(x,'highpass',75)
    i=int(st*SR); m=min(len(x),N-i); vo[0,i:i+m]+=x[:m]; vo[1,i:i+m]+=x[:m]; iv.append((st,st+len(x)/SR))
vo/=np.max(np.abs(vo))+1e-9; vo=np.tanh(vo*1.25)/np.tanh(1.25)   # one gain for all cuts keeps the take's natural levels
vo=room(vo,.05,1.0)
duck=np.ones(N); tt=np.arange(N)/SR
for a,b in iv:
    g=np.clip(np.minimum((tt-(a-.2))/.2,((b+.35)-tt)/.35),0,1); duck=np.minimum(duck,1-.72*g)
mix=music*duck*.27+sfx+vo*.9
e=int(END*SR); fo=int(.8*SR); mix[:,e-fo:e]*=np.linspace(1,0,fo)**1.5; mix=mix[:,:e]; mix/=np.max(np.abs(mix))*1.05
wavfile.write('sizzle_mix_raw.wav',SR,(mix.T*32767).astype(np.int16)); print('ok',END)
