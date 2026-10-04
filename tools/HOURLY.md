# AIMTV hourly live refresh: runbook

Goal: keep the channel live. Every hour, replace the news bulletin (`tdty`), the taxi report (`meter`), one rotating story programme, and the ticker, voiced and pushed to GitHub. The channel and the YouTube stream pick it up on their own within a few minutes. No other files are touched.

## Steps
1. Work in the `JointRobot/aimtv-tv` repo (public). Pull the latest `main`. Read `tools/canon.md` (style guide) and `site/live/live.json` (what is on air now, for continuity).
2. Find today's news (current date in IST). Use web search for: India top stories, world top stories, technology, business, sports, entertainment, weather and festival news. Prefer 2 to 3 sources for each item you use; if a fact is unconfirmed, skip it. Never use tragedies, deaths, violence, crime victims or communal topics as material. Keep real-world facts accurate; the jokes are about 2041.
3. Write `draft.json` (format at the top of `tools/live_build.py`):
   - `tdty`: 8 lines, new items (not last hour's), stamp `Archived · <d> <Mon> 2026`.
   - `meter`: 5 lines, reacting to the same news from the taxi, stamp `Live · Shivajinagar`.
   - one rotating programme chosen by the IST hour: hour mod 5 = 0 `shop`, 1 `travel`, 2 `ad1`, 3 `psa`, 4 `baba`. Format and length as in `tools/canon.md`.
   - `ticker`: 8 to 12 items.
4. Run `python3 tools/live_build.py draft.json`. It checks speakers and lengths, makes the voice clips and rewrites `site/live/live.json`. If it errors, fix the draft and rerun. If ffmpeg is missing flite, `apt-get install -y ffmpeg` (or report it).
5. Check: `site/live/live.json` has the new `v`, the clip files exist, `git status` shows only `site/live/` changes.
6. Commit with message `live <v>` and push to `main`. If the push is rejected, `git pull --rebase` and push again. Never touch other files.
7. Reply with one line: what is now on air (the three headlines used). If news search is unavailable, still refresh the ticker and the rotating programme and say so.
