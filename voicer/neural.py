#!/usr/bin/env python3
"""Neural Indian-accent voices for AIMTV, run on the stream server (not needed anywhere else).
Reads the text of every voice clip (site/vo/manifest.json and site/live/live.json), speaks it with Piper
(CMU Arctic / L2-ARCTIC Indian speakers), and builds /opt/aimtv/serve = site + neural clips on top.
Clips it cannot make stay as the original recordings. Safe to run every few minutes."""
import signal, os, sys, json, re, hashlib, subprocess, shutil, wave, time
REPO = "/opt/aimtv/repo/site"; NE = "/opt/aimtv/neural"; SERVE = "/opt/aimtv/serve"
VOICES = "/opt/aimtv/voices"
MODELS = {"arctic": "en_US-arctic-medium", "l2": "en_US-l2arctic-medium"}
# who: (model, speaker id, pitch factor, tempo).  arctic: ksp 3, slp 12, aup 13, gka 17.  l2arctic Hindi: SVBI 2, TNI 9, ASI 10, RRBI 19
CAST = {
 "hema": ("l2", 9, 1.00, 1.00), "sarla": ("l2", 9, 1.10, 1.06), "lata": ("arctic", 12, 0.97, 1.04),
 "mrst": ("arctic", 12, 1.05, 0.95), "devi": ("l2", 9, 0.93, 0.98), "tabla": ("arctic", 12, 1.00, 1.00),
 "jc": ("l2", 10, 1.00, 1.00), "tchu": ("arctic", 3, 0.95, 1.05), "animation": ("arctic", 17, 1.12, 1.08),
 "fadarr": ("l2", 19, 0.86, 0.92),
}  # chaibot stays the robot voice; baba never speaks
CASTV = "1"
SAY = [("AIMTV", "A I M T V"), ("Tabla Nari", "Tubla Naari"), ("Bandre 3000", "Bandra three thousand"), ("Tchu Tchu", "Choo Choo"),
       ("Hema", "Hay-ma"), ("Juhu Chaiwala", "Joohoo Chai-waala"), ("Bombai", "Bombay"), ("Hindia", "Hindia"), ("Fa Corp", "Faa Corp"),
       ("Fa King", "Faa King"), ("Fa Cough", "Faa Cough"), ("Fa Darr", "Faa Dar"), ("Rama Tuta", "Raama Toota"), ("Shivajinagar", "Shivaji nagar"),
       ("Namaste", "Namastay"), ("Lonavala", "Lonavla"), ("Matheran", "Maatheran"), ("Daman", "Damann"), ("chikki", "chikki"), ("Challo", "Chalo")]
def say(t):
    for a, b in SAY: t = t.replace(a, b)
    return t

def entries():
    e = {}
    p = os.path.join(REPO, "vo/manifest.json")
    if os.path.exists(p):
        for name, (who, text) in json.load(open(p)).items(): e["vo/%s.mp3" % name] = (who, text)
    p = os.path.join(REPO, "live/live.json")
    if os.path.exists(p):
        for pid, pr in json.load(open(p)).get("progs", {}).items():
            for i, l in enumerate(pr.get("lines", [])): e["%s%d.mp3" % (pr["clips"], i)] = (l[0], l[1])
    return e

def _t(*a): raise TimeoutError('clip took too long')
signal.signal(signal.SIGALRM, _t)
def main():
    os.makedirs(NE, exist_ok=True); st_p = os.path.join(NE, "state.json")
    st = json.load(open(st_p)) if os.path.exists(st_p) else {}
    ent = entries(); todo = []
    for path, (who, text) in ent.items():
        if who not in CAST: continue
        key = hashlib.sha1(("%s|%s|%s" % (CASTV, who, text)).encode()).hexdigest()[:12]
        if st.get(path) != key or not os.path.exists(os.path.join(NE, path)): todo.append((path, who, text, key))
    if todo:
        from piper import PiperVoice, SynthesisConfig
        vs = {}
        for path, who, text, key in todo:
            m, sid, k, tempo = CAST[who]
            try:
                signal.alarm(120)
                if m not in vs: vs[m] = PiperVoice.load(os.path.join(VOICES, MODELS[m] + ".onnx"))
                tmp = "/tmp/nv_%d.wav" % os.getpid()
                with wave.open(tmp, "wb") as w: vs[m].synthesize_wav(say(text), w, syn_config=SynthesisConfig(speaker_id=sid))
                t = tempo / k; chain = ["asetrate=%d" % int(22050 * k), "aresample=22050"]
                while t > 2: chain.append("atempo=2.0"); t /= 2
                while t < .5: chain.append("atempo=0.5"); t /= .5
                chain += ["atempo=%.4f" % t, "highpass=f=70", "silenceremove=start_periods=1:start_threshold=-50dB",
                          "areverse", "silenceremove=start_periods=1:start_threshold=-50dB", "areverse", "loudnorm=I=-17:TP=-2"]
                out = os.path.join(NE, path); os.makedirs(os.path.dirname(out), exist_ok=True)
                subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", tmp, "-af", ",".join(chain), "-ar", "22050", "-ac", "1",
                                "-c:a", "libmp3lame", "-b:a", "48k", out], check=True)
                signal.alarm(0); st[path] = key
            except BaseException as ex:
                signal.alarm(0)
                print("skip", path, ex, file=sys.stderr)
            if len([1 for _ in st]) % 10 == 0: json.dump(st, open(st_p, "w"))
        json.dump(st, open(st_p, "w"))
    # drop neural files no longer referenced
    for path in list(st):
        if path not in ent:
            try: os.remove(os.path.join(NE, path))
            except OSError: pass
            st.pop(path)
    json.dump(st, open(st_p, "w"))
    # serve = site + neural overlay
    os.makedirs(SERVE, exist_ok=True)
    subprocess.run(["rsync", "-a", "--delete", REPO + "/", SERVE + "/"], check=True)
    subprocess.run(["rsync", "-a", "--exclude=state.json", NE + "/", SERVE + "/"], check=True)
    print("neural: %d made, %d total" % (len(todo), len(st)))
main()
