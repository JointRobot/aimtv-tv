# AIMTV — 24/7 live stream to YouTube

This repo is what the AIMTV stream server plays. `site/` is the channel (receiver + songs + voices).
Push a new `site/` and the server picks it up within 5 minutes.

Server setup (once, on a fresh Ubuntu server):

    curl -fsSL https://raw.githubusercontent.com/JointRobot/aimtv-tv/main/setup.sh | sudo bash -s -- YOUR-STREAM-KEY

Check it: `systemctl status aimtv` · logs: `journalctl -u aimtv -f`

## Public site on Cloudflare Pages
- Pages project connected to this repo: no build command, build output directory `site`. `functions/api/score.js` is picked up automatically as the Fame Meter API.
- D1 database bound to the project with the variable name `DB` (the table is created on first use). Without it the site still works and the Fame Meter counts per browser.
- `site/_headers` (written by `build.sh`) keeps `live/` uncached so the two-hourly refresh shows up at once.
- The 24/7 YouTube stream cannot run on Cloudflare; it runs on the server set up by `setup.sh`, from this same repo.

## Voices on the stream server
The stream's browser has no Indian voices, so `voicer/neural.py` (Piper, Indian-accent English speakers) re-voices every clip listed in
`site/vo/manifest.json` and `site/live/live.json` and serves `/opt/aimtv/serve` = site + neural clips. Casting is the `CAST` table in neural.py.
After changing speech in the receiver, run `python3 mk_manifest.py` (in the folder above) before build.sh. One-time server install: python venv at
/opt/aimtv/tts with `piper-tts`, voices en_US-arctic-medium and en_US-l2arctic-medium in /opt/aimtv/voices, `apt install rsync`.
