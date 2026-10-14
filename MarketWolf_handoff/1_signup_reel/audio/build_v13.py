import json, sys, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

DK = sys.argv[1]
SR = 44100
D = json.load(open('events.json')); CF = D['CFG']
VO = json.load(open(f'v13/{DK}/vo.json'))
END, OUT, S = D['END'], D['OUT'], D['S']
N = int(END * SR) + SR
rng = np.random.default_rng(3)
BAR = 2.0

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

# D major, lounge voicings
CH = [[57, 61, 64, 66], [54, 57, 61, 62], [54, 57, 59, 62], [55, 59, 62, 64]]   # Dmaj9 Bm9 Gmaj9 A6sus
BASS = [38, 35, 31, 33]
music = np.zeros((2, N)); perc = np.zeros((2, N))

# intro: pad swell + single chord, no drums
STEP0 = D['STEP0']
p = pad([50] + CH[0], STEP0 + 1.0)
music[:, :p.shape[1]] += p * .9
place(music, chord_hit(CH[0], 3.5, .7), .2, .55, -.15)
place(music, bell(81, 3.0), .25, .07, .3)                       # logo appears

# main bed from STEP0 to OUT
t, bar = STEP0 - .2, 0
while t < OUT - .01:
    ci = (bar // 1) % 4
    place(music, chord_hit(CH[ci], 2.2, .75), t, .5, -.15)
    place(music, chord_hit(CH[ci][1:], 1.0, .45), t + 1.25, .35, .2)  # soft offbeat comp
    place(music, sub(BASS[ci], 2.0), t, .55)
    pp = pad(CH[ci], 2.4); place(music, pp[0], t, .35, -.6); place(music, pp[1], t, .35, .6)
    if bar >= 1:  # whisper of rhythm
        place(perc, soft_kick(), t, .35)
        for e in range(8): place(perc, brush(), t + e * .25, .08 + .05 * (e % 2), .35 if e % 2 else -.35)
    if bar % 4 == 3: place(music, rhodes(CH[ci][-1] + 12, 1.5, .4), t + 1.5, .12, .4)  # tiny turnaround note
    t += BAR; bar += 1
# outro: resolve on Dmaj9, soft bell with the logo
fin = OUT
po = pad([50] + CH[0], END - fin)
place(music, po[0], fin, .9, -.3); place(music, po[1], fin, .9, .3)
place(music, chord_hit(CH[0] + [69], 4.0, .65), fin + .75, .5)
place(music, bell(81, 4.0), fin + .8, .09, -.2); place(music, bell(86, 4.0), fin + .95, .06, .25)
music = room(music + perc * .9, .2)

# ---------- SFX: barely there ----------
sfx = np.zeros((2, N))
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
for e in D['ev']:
    t, ty = e['t'], e['type']
    if ty == 'key': place(sfx, tap(), t, .22, rng.uniform(-.1, .1))
    elif ty == 'select': place(sfx, tap(), t, .25)
    elif ty == 'cta': place(sfx, tock(), t, .3)
    elif ty in ('whoosh', 'reveal'): place(sfx, swish(), t - .05, .12, .2)
place(sfx, swish(.8), D['PIN_IN'], .12, -.2)
place(sfx, swish(.8), OUT + .05, .1, .2)

# ---------- VO ----------
vo = np.zeros((2, N)); iv = []
DS = CF['VO']['draft_starts'][DK]
base = {'intro': 0, 's1': S[0], 's2': S[1], 's3': S[2], 's4': S[3], 's5': S[4], 's6': S[5], 's7': S[6], 'o1': OUT, 'o2': OUT}
for k, rel in DS.items():
    st = base[k] + rel
    sr, x = wavfile.read(f'v13/{DK}/{k}.wav'); x = x.astype(np.float64) / 32768
    x = filt(x, 'highpass', 75)  # one take: keep its natural relative levels
    x = np.tanh(x * 1.25) / np.tanh(1.25)       # gentle glue, no squash
    i = int(st * SR); m = min(len(x), N - i)
    vo[0, i:i + m] += x[:m]; vo[1, i:i + m] += x[:m]; iv.append((st, st + len(x) / SR))
vo = room(vo, .05, 1.0)

# ---------- mix ----------
duck = np.ones(N); tt = np.arange(N) / SR
for a, b in iv:
    g = np.clip(np.minimum((tt - (a - .25)) / .25, ((b + .5) - tt) / .5), 0, 1); duck = np.minimum(duck, 1 - .7 * g)
mix = music * duck * .26 + sfx + vo * .9
if len(sys.argv)>2:
    for a,b in iv[3:6]:
        i,j=int(a*SR),int(b*SR); r=lambda z: 20*np.log10(np.sqrt((z[:,i:j]**2).mean())+1e-9)
        print('voice %.1f  music-under %.1f  diff %.1f dB'%(r(vo*.9),r(music*duck*.26),r(vo*.9)-r(music*duck*.26)))
e = int(END * SR); fo = int(1.2 * SR); mix[:, e - fo:e] *= np.linspace(1, 0, fo) ** 1.5; mix = mix[:, :e]
mix /= np.max(np.abs(mix)) * 1.05
wavfile.write(f'mix_v13_{DK}_raw.wav', SR, (mix.T * 32767).astype(np.int16))
print('ok', DK, END, {k: round(base[k] + v, 2) for k, v in DS.items()})
