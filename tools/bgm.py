"""Generate a soft lo-fi BGM track (royalty-free, synthesized) as WAV.
usage: python3 bgm.py out.wav seconds [seed] [mood]
mood: calm (default) | bright
Variation (2026-11-18, user: "every Short should be different"): the seed picks the key, the chord progression,
the drum feel and the melody pattern, so consecutive Shorts don't share the same track. Tempo stays per mood
(BPM must match make_reel.py's beat grid).
"""
import sys, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100

def note_freq(n):  # midi -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)

def epiano(freq, dur, vel=0.25):
    t = np.arange(int(SR * dur)) / SR
    env = np.exp(-t * 2.2) * (1 - np.exp(-t * 80))
    tone = (np.sin(2*np.pi*freq*t) + 0.35*np.sin(2*np.pi*2*freq*t)*np.exp(-t*4)
            + 0.12*np.sin(2*np.pi*3*freq*t)*np.exp(-t*6))
    trem = 1 + 0.08*np.sin(2*np.pi*4.5*t)
    return vel * tone * env * trem

def kick(dur=0.35):
    t = np.arange(int(SR*dur))/SR
    f = 110*np.exp(-t*18)+45
    return 0.7*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)

def hat(rng, dur=0.06):
    t = np.arange(int(SR*dur))/SR
    b, a = butter(2, 7000/(SR/2), 'high')
    return 0.12*lfilter(b, a, rng.standard_normal(len(t)))*np.exp(-t*60)

def snare(rng, dur=0.18):
    t = np.arange(int(SR*dur))/SR
    b, a = butter(2, [1500/(SR/2), 6000/(SR/2)], 'band')
    return 0.22*lfilter(b, a, rng.standard_normal(len(t)))*np.exp(-t*22)

def add(buf, x, start):
    i = int(start*SR)
    if i >= len(buf): return
    x = x[:len(buf)-i]
    buf[i:i+len(x)] += x

def make(seconds, seed=1, mood="calm"):
    rng = np.random.default_rng(seed)
    bpm = 84 if mood == "calm" else 96
    beat = 60/bpm
    n = int(SR*(seconds+2))
    mus = np.zeros(n); drm = np.zeros(n)
    progs = {
        "calm": [
            [[53,57,60,64],[52,55,59,62],[50,53,57,60],[48,52,55,59]],  # Fmaj7 Em7 Dm7 Cmaj7
            [[50,53,57,60],[55,59,62,65],[48,52,55,59],[57,60,64,67]],  # Dm7 G7 Cmaj7 Am7
            [[45,48,52,55],[53,57,60,64],[48,52,55,59],[55,59,62,65]],  # Am7 Fmaj7 Cmaj7 G7
        ],
        "bright": [
            [[48,52,55,59],[57,60,64,67],[53,57,60,64],[55,59,62,65]],  # Cmaj7 Am7 Fmaj7 G7
            [[53,57,60,64],[55,59,62,65],[52,55,59,62],[57,60,64,67]],  # Fmaj7 G7 Em7 Am7
            [[48,52,55,59],[55,59,62,65],[57,60,64,67],[53,57,60,64]],  # Cmaj7 G7 Am7 Fmaj7
        ],
    }
    opts = progs.get(mood, progs["calm"])
    shift = [0, 2, -3, 5, -2][seed % 5]                 # key
    prog = [[m + shift for m in ch] for ch in opts[(seed // 5) % len(opts)]]
    feel = (seed // 15) % 3                             # 0 straight, 1 half-time, 2 swung hats
    arp = (seed // 2) % 2 == 1                          # melody: off-beat plucks or a soft 8th-note arpeggio
    swing = beat * (0.58 if feel == 2 else 0.5)
    bar = 4*beat
    t = 0.0; ci = 0
    while t < seconds + 1:
        ch = prog[ci % len(prog)]
        for k, m in enumerate(ch):
            add(mus, epiano(note_freq(m), bar*1.1, 0.16), t + k*0.018)
        add(mus, epiano(note_freq(ch[0]-12), bar, 0.22), t)          # bass
        if arp:
            for b in range(8):
                m = ch[(b + ci) % 4] + 12
                add(mus, epiano(note_freq(m), beat*0.9, 0.045), t + b*beat/2 + rng.uniform(0, 0.02))
        else:   # little melody pluck on beats 2 and 4
            for b in (1, 3):
                m = ch[rng.integers(1, 4)] + 12
                add(mus, epiano(note_freq(m), beat*1.5, 0.07), t + b*beat + rng.uniform(0, 0.03))
        for b in range(4):
            bt = t + b*beat
            if feel == 1:
                if b == 0: add(drm, kick(), bt)
                if b == 2: add(drm, snare(rng), bt)
            else:
                if b in (0, 2): add(drm, kick(), bt)
                if b in (1, 3): add(drm, snare(rng), bt)
            add(drm, hat(rng), bt + swing)
            add(drm, hat(rng)*0.6, bt)
        t += bar; ci += 1
    # soften drums (lo-fi)
    b, a = butter(2, 5000/(SR/2), 'low'); drm = lfilter(b, a, drm)
    mix = mus + 0.55*drm
    # simple echo for space
    d = int(0.28*SR); echo = np.zeros_like(mix); echo[d:] = mix[:-d]*0.25
    mix = mix + echo
    b, a = butter(2, 7500/(SR/2), 'low'); mix = lfilter(b, a, mix)
    # vinyl hiss
    mix += 0.004*rng.standard_normal(len(mix))
    mix = mix[:int(SR*seconds)]
    # fades
    fi, fo = int(0.5*SR), int(1.5*SR)
    mix[:fi] *= np.linspace(0, 1, fi); mix[-fo:] *= np.linspace(1, 0, fo)
    mix = mix/np.max(np.abs(mix))*0.8
    st = np.stack([mix, np.roll(mix, int(0.012*SR))], axis=1)
    return (st*32767).astype(np.int16)

if __name__ == "__main__":
    out = sys.argv[1]; secs = float(sys.argv[2])
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    mood = sys.argv[4] if len(sys.argv) > 4 else "calm"
    wavfile.write(out, SR, make(secs, seed, mood))
    print("wrote", out)
