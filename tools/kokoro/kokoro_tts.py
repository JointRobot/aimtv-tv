"""Hindi + English (Hinglish) voices for the AIMTV live desk and receiver clips.
Kokoro-82M (ONNX) with the bundled espeak-ng for Hindi pronunciation. Needs only numpy + onnxruntime.
The 350 MB model files are fetched once from GitHub and cached in ~/.cache/aimtv-kokoro.
    python3 kokoro_tts.py WHO "देवनागरी text" out.mp3
Speakers: see KCAST. Text must be Devanagari (English words spelled the way they sound in Devanagari)."""
import os, sys, json, subprocess, wave, tempfile, urllib.request
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.expanduser("~/.cache/aimtv-kokoro")
REL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
MODEL, VOICES = "kokoro-v1.0.onnx", "voices-v1.0.bin"
# who: (kokoro voice, speed, pitch factor, extra ffmpeg filter)
KCAST = {
    "hema": ("hf_alpha", 1.0, 1.0, ""), "devi": ("hf_alpha", 1.1, 0.94, ""),
    "lata": ("hf_beta", 1.0, 1.0, ""), "mrst": ("hf_beta", 0.9, 1.03, ""),
    "jc": ("hm_omega", 1.0, 1.0, ""), "tchu": ("hm_omega", 0.96, 0.9, ""),
    "sarla": ("hf_alpha", 1.05, 1.1, ""), "dimpy": ("hf_beta", 1.08, 1.12, ""),
    "chaibot": ("hm_psi", 1.2, 1.18, "aecho=0.8:0.6:12:0.4"),
    "animation": ("hm_omega", 0.93, 1.0, ""),  # Marathi dog: Marathi (Devanagari) text read by the Hindi voice engine
}
_S = {}

def _fetch(name):
    os.makedirs(CACHE, exist_ok=True); p = os.path.join(CACHE, name)
    if not os.path.exists(p) or os.path.getsize(p) < 1000000:
        tmp = p + ".part"; urllib.request.urlretrieve(REL + name, tmp); os.replace(tmp, p)
    return p

def available():
    try:
        try: import onnxruntime  # noqa
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", "onnxruntime"], check=True); import onnxruntime  # noqa
        subprocess.run([ESP, "--version"], env=_env(), capture_output=True, check=True)
        _fetch(MODEL); _fetch(VOICES); return True
    except Exception as e:
        print("kokoro unavailable:", e, file=sys.stderr); return False

ESP = os.path.join(HERE, "espeak", "bin", "espeak-ng")
def _env():
    return dict(os.environ, LD_LIBRARY_PATH=os.path.join(HERE, "espeak", "lib"), ESPEAK_DATA_PATH=os.path.join(HERE, "espeak", "data"))

def _load():
    if not _S:
        import onnxruntime as ort
        _S["s"] = ort.InferenceSession(_fetch(MODEL), providers=["CPUExecutionProvider"])
        _S["v"] = np.load(_fetch(VOICES)); _S["vocab"] = json.load(open(os.path.join(HERE, "vocab.json")))
    return _S

def phonemes(text, lang="hi"):
    r = subprocess.run([ESP, "-v", lang, "-q", "--ipa=3", "--sep=", "-b", "1", text], capture_output=True, text=True, env=_env(), check=True)
    import re; return " ".join(re.sub(r"\([a-z]{2,3}\)", "", r.stdout.replace("_", "").replace("\u200d", "")).split())

def _wave(text, voice, speed, lang="hi"):
    S = _load(); ids = [S["vocab"][c] for c in phonemes(text, lang) if c in S["vocab"]][:510]
    style = S["v"][voice][len(ids)].astype(np.float32)
    return S["s"].run(None, {"tokens": np.array([[0] + ids + [0]], dtype=np.int64), "style": style, "speed": np.array([speed], dtype=np.float32)})[0].squeeze()

# English-speaking cast (English text, not Devanagari): who: (kokoro voice, speed, pitch factor, extra ffmpeg filter)
PHRASED = {"animation"}
KEN = {"tabla": ("af_heart", 0.97, 0.98, "")}

def speak(text, who, out, bitrate="40k"):
    lang = "hi"  # the bundled espeak only has Hindi; it reads Roman English words through its own English dictionary
    voice, speed, k, fx = (KEN if who in KEN else KCAST)[who]
    if who in PHRASED:  # short phrases with small pauses sound far less robotic than one long breath
        import re
        parts = [x.strip() for x in re.split(r"(?<=[.?!।])\s+", text) if x.strip()]
        gap = np.zeros(int(24000 * .22), dtype=np.float32)
        a = np.concatenate([np.concatenate([_wave(x, voice, speed, lang), gap]) for x in parts])
    else:
        a = _wave(text, voice, speed, lang)
    wav = tempfile.mktemp(suffix=".wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())
    chain = []
    if abs(k - 1) > .001: chain += ["asetrate=%d" % int(24000 * k), "aresample=24000", "atempo=%.4f" % (1 / k)]
    chain += ["highpass=f=70", "silenceremove=start_periods=1:start_threshold=-50dB", "areverse",
              "silenceremove=start_periods=1:start_threshold=-50dB", "areverse"]
    if fx: chain.append(fx)
    chain.append("loudnorm=I=-17:TP=-2")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", wav, "-af", ",".join(chain), "-ar", "24000", "-ac", "1",
                    "-c:a", "libmp3lame", "-b:a", bitrate, out], check=True)
    os.remove(wav)

if __name__ == "__main__":
    speak(sys.argv[2], sys.argv[1], sys.argv[3]); print("ok", sys.argv[3])
