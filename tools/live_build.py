#!/usr/bin/env python3
"""AIMTV live refresh: turn a text draft into voiced clips + live.json for the broadcast site.

usage: python3 tools/live_build.py draft.json
draft.json = {"ticker": ["HEADLINE", ...],
              "progs": {"tdty": {"stamp": "Archived · 5 Oct 2026", "lines": [["hema", "English text", "", "regional-language line"], ...]}, "meter": {...}}}
Writes site/live/live.json and site/live/<prog>_<version>_<n>.mp3. Programmes missing from the draft keep their
previous content. Old clips no longer referenced are deleted. Needs ffmpeg with flite.
"""
import os, sys, json, re, subprocess, datetime
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site", "live")
ALLOWED = {"tdty", "meter", "shop", "travel", "ad1", "psa"}  # baba is founder-written only
SAY = [('AIMTV', 'A I M T V'), ('Hema', 'Hayma'), ('Namaste', 'Nuh muh stay'), ('Namaskara', 'Numuskaara'), ('Namaskar', 'Numuskaar'), ('Juhu Chaiwala', 'Joo hoo Chai waala'), ('Tchu Tchu', 'Choo Choo'), ('Shivajinagar', 'Shivaaji nugger'), ('Bombai', 'Bom bye'), ('Challo', 'Chullo'), ('Fa King', 'Faa King'), ('Fa Corp', 'Faa Corp'), ('Fa Cough', 'Faa Cough'), ('Fa Darr', 'Faa Dar'), ('Rama Tuta', 'Raama Toota'), ('Lonavala', 'Lo naa vuh luh'), ('chikki', 'chick ee'), ('Kem cho', 'Kem cho'), ('Sat Sri Akal', 'Sut Shree Akaal'), ('Jhulelal', 'Jhoolay laal'), ('babuji', 'baabu jee'), ('Bhenji', 'Bhen jee'), ('dosa', 'doe saa'), ('Matheran', 'Maa thay run'), ('Daman', 'Duh mun'), ('Aichi', 'Eye chee'), ('Legato', 'Leh gah toe'), ('2.0', 'two point oh'), ('2026', 'twenty twenty six'), ('2041', 'twenty forty one'), ('Sarla', 'Sur laa'), ('Malini', 'Maa li nee')]
CAST = {'hema': ('slt', 1.0, 0.98), 'sarla': ('slt', 1.1, 1.06), 'lata': ('slt', 0.94, 1.06), 'mrst': ('slt', 1.04, 0.94), 'devi': ('slt', 0.92, 1.0), 'jc': ('rms', 1.0, 1.0), 'chaibot': ('rms', 1.22, 1.12), 'tchu': ('kal16', 0.92, 0.95), 'animation': ('kal16', 1.28, 1.04), 'fadarr': ('awb', 0.84, 0.88), 'baba': ('awb', 0.7, 0.8), 'tabla': ('slt', 1.0, 1.0)}

def say(t):
    for a, b in SAY: t = t.replace(a, b)
    return t

def clip(job):
    path, who, text = job
    voice, k, tempo = CAST[who]
    txt = path + ".txt"; open(txt, "w").write(say(text))
    t = tempo / k; chain = ["asetrate=%d" % int(16000 * k), "aresample=22050"]
    while t > 2: chain.append("atempo=2.0"); t /= 2
    while t < .5: chain.append("atempo=0.5"); t /= .5
    chain += ["atempo=%.4f" % t, "highpass=f=70", "silenceremove=start_periods=1:start_threshold=-50dB",
              "areverse", "silenceremove=start_periods=1:start_threshold=-50dB", "areverse", "loudnorm=I=-17:TP=-2"]
    if who == "chaibot": chain.insert(-1, "aecho=0.8:0.6:12:0.4")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "flite=textfile=%s:voice=%s" % (txt, voice),
                    "-af", ",".join(chain), "-ar", "22050", "-ac", "1", "-c:a", "libmp3lame", "-b:a", "40k", path], check=True)
    os.remove(txt)
    return path

def main(draft_path):
    draft = json.load(open(draft_path))
    os.makedirs(OUT, exist_ok=True)
    lj = os.path.join(OUT, "live.json")
    live = json.load(open(lj)) if os.path.exists(lj) else {"progs": {}}
    now = datetime.datetime.now(datetime.timezone.utc)
    ver = now.strftime("%Y%m%dT%H%M")
    jobs = []
    for pid, p in (draft.get("progs") or {}).items():
        if pid not in ALLOWED: raise SystemExit("unknown programme: " + pid)
        lines = p["lines"]
        if not 3 <= len(lines) <= 12: raise SystemExit(pid + ": need 3-12 lines")
        clean = []
        for i, l in enumerate(lines):
            who, text = l[0], re.sub(r"\s+", " ", l[1]).strip()
            en = l[2] if len(l) > 2 else ""
            rg = re.sub(r"\s+", " ", l[3]).strip() if len(l) > 3 and l[3] else ""
            if len(rg) > 400: raise SystemExit("%s line %d: regional line over 400 chars" % (pid, i))
            if who not in CAST: raise SystemExit("unknown speaker: " + who)
            if not text or len(text) > 260: raise SystemExit("%s line %d: empty or over 260 chars" % (pid, i))
            if re.search(r"https?://|www\.", text): raise SystemExit("%s line %d: no links in speech" % (pid, i))
            clean.append([who, text, en, rg])
            jobs.append((os.path.join(OUT, "%s_%s_%d.mp3" % (pid, ver, i)), who, text))
        live["progs"][pid] = {"stamp": p.get("stamp", ""), "lines": clean, "clips": "live/%s_%s_" % (pid, ver)}
    if jobs:
        with ThreadPoolExecutor(4) as ex: list(ex.map(clip, jobs))
    if draft.get("ticker"):
        live["ticker"] = [re.sub(r"\s+", " ", str(x)).strip().upper() for x in draft["ticker"] if str(x).strip()][:14]
    live["v"] = ver; live["updated"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump(live, open(lj, "w"), ensure_ascii=False, indent=1)
    keep = {os.path.basename(p["clips"]) for p in live["progs"].values()}
    for f in os.listdir(OUT):
        if f.endswith(".mp3") and not any(f.startswith(k) for k in keep): os.remove(os.path.join(OUT, f))
    print("live", ver, len(jobs), "clips,", len(live.get("ticker", [])), "ticker items")

if __name__ == "__main__":
    main(sys.argv[1])
