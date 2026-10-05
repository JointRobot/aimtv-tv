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
