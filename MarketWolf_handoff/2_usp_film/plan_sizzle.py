# Sizzle cut (25-30s). Builds the VO edit from the approved Viraj takes in vo/,
# cutting at the quietest 10 ms inside each sentence gap, then writes
# sizzle/vo/*.wav, sizzle/timeline.json and sizzle/timing.js.
# Run from 2_usp_film/:  python3 plan_sizzle.py
import json, re, os, numpy as np
from scipy.io import wavfile
V = json.load(open('vo/vo.json')); SR = 44100; FADE = .012
os.makedirs('sizzle/vo', exist_ok=True)

def wav(k):
    sr, x = wavfile.read(f'vo/{k}.wav'); assert sr == SR
    return x.astype(np.float64) / 32768
def word(k, prefix, n=1):
    c = 0
    for i, (w, a, b) in enumerate(V[k]['words']):
        if re.sub(r'[^a-z0-9]', '', w.lower()).startswith(prefix):
            c += 1
            if c == n: return i
    raise KeyError((k, prefix, n))
def quiet(x, a, b):
    """time of the quietest 10 ms window between a and b (s)"""
    w = int(.01 * SR); i0, i1 = int(a * SR), int(b * SR)
    e = [np.sqrt(np.mean(x[i:i + w] ** 2)) for i in range(i0, max(i0 + 1, i1 - w), int(.002 * SR))]
    return (i0 + int(np.argmin(e)) * int(.002 * SR) + w // 2) / SR
def gap(k, i):
    """cut point between word i-1 and word i"""
    W = V[k]['words']; return quiet(wav(k), W[i - 1][1] + .5 * (W[i - 1][2] - W[i - 1][1]), W[i][1] + .03)

# segment = (name, source take, first word index, first word index after the segment or None)
SEG = [
    ('hook',   'l1', 0, None),                       # Every trader knows when to get in. Very few know when to get out.
    ('xf',     'l3', 0, word('l3', 'a')),            # On MarketWolf, every trade has its exit set before you enter.
    ('exit',   'l3', word('l3', 'a'), None),         # A target to book your profit, and a stop loss to protect your capital.
    ('ideas',  'l4', word('l4', 'trade'), word('l4', 'each')),  # trade ideas from SEBI-registered analysts
    ('app',    'l5', 0, word('l5', 'even')),         # Indices, stocks and commodities, all in one app.
    ('price',  'l6', 0, None),                       # A flat nineteen rupees a trade. Zero AMC. Nothing hidden.
    ('end',    'l8', 0, None),                       # MarketWolf. Trade with discipline.
]
PRE = {'hook': .25}                    # silence before the line inside its scene
GAP_AFTER = {'hook': .25, 'exit': .45, 'end': 1.05}   # breath after the line before the next scene starts
DEF_GAP = .18

S, VO, CUE, SEGS, t = [], {}, {}, {}, 0.0
for name, k, i0, i1 in SEG:
    x = wav(k); W = V[k]['words']
    a = 0.0 if i0 == 0 else gap(k, i0)
    b = len(x) / SR if i1 is None else gap(k, i1)
    y = x[int(a * SR):int(b * SR)].copy()
    # trim trailing near-silence so gaps are controlled here, not by the take
    env = np.abs(y); thr = .01 * env.max(); last = np.nonzero(env > thr)[0][-1]
    y = y[:min(len(y), last + int(.06 * SR))]
    f = int(FADE * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    wavfile.write(f'sizzle/vo/{name}.wav', SR, (y * 32767).astype(np.int16))
    dur = len(y) / SR
    S.append(round(t, 3)); st = t + PRE.get(name, .12); VO[name] = round(st, 3)
    SEGS[name] = {'src': k, 'from': round(a, 3), 'to': round(b, 3), 'dur': round(dur, 3),
                  'text': ' '.join(w for w, _, _ in W[i0:(i1 if i1 is not None else len(W))])}
    for j, (w, wa, wb) in enumerate(W[i0:(i1 if i1 is not None else len(W))]):
        key = f"{name}_{re.sub(r'[^a-z0-9]', '', w.lower())}"
        n = 2
        while key in CUE: key = f"{name}_{re.sub(r'[^a-z0-9]', '', w.lower())}{n}"; n += 1
        CUE[key] = round(st + wa - a, 3)
    CUE[f'{name}_end'] = round(st + dur, 3)
    t = st + dur + GAP_AFTER.get(name, DEF_GAP)
END = round(t, 2)
json.dump({'S': S, 'END': END, 'VO': VO, 'CUE': CUE, 'SEG': SEGS}, open('sizzle/timeline.json', 'w'), indent=1)
open('sizzle/timing.js', 'w').write('window.TL=' + json.dumps({'S': S, 'END': END, 'CUE': CUE}) + ';')
print('scenes', S, 'END', END)
for n, s in SEGS.items(): print(f'  {n:6s} {VO[n]:6.2f}s  {s["dur"]:.2f}s  {s["text"]}')
