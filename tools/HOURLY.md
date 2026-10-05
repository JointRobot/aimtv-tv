# AIMTV live refresh (every two hours): runbook

Goal: keep the channel live. Every two hours, replace the news bulletin (`tdty`), the taxi report (`meter`), JC's tech desk (`shop`), one rotating story programme, and the ticker, voiced and pushed to GitHub. The channel and the YouTube stream pick it up on their own within a few minutes. No other files are touched.

## Steps
1. Work in the `JointRobot/aimtv-tv` repo (public). Pull the latest `main`. Read `tools/canon.md` (style guide) and `site/live/live.json` (what is on air now, for continuity).
2. Find today's news (current date in IST). Use web search for: India top stories, world top stories, technology, business, sports, entertainment, weather and festival news. Prefer 2 to 3 sources for each item you use; if a fact is unconfirmed, skip it. Never use tragedies, deaths, violence, crime victims or communal topics as material. Keep real-world facts accurate; the jokes are about 2041.
3. Write `draft.json` (format at the top of `tools/live_build.py`):
   - `tdty`: 8 lines, new items (not the last bulletin's), stamp `Archived · <d> <Mon> 2026`.
   - `meter`: 5 lines, reacting to the same news from the taxi, stamp `Live · Shivajinagar`.
   - `shop`: JC's tech desk from the day's real tech news, stamp `Tech desk · <d> <Mon> 2026`.
   - one rotating programme chosen by the IST hour: (hour // 2) mod 3 = 0 `travel`, 1 `ad1`, 2 `psa` (never `baba`: his lines are founder-written). Format and length as in `tools/canon.md`.
   - every line is `[speaker, English text, "", regional line]`: the fourth field is the line in the speaker's home language and script (see "Regional line" in `tools/canon.md`).
   - `ticker`: 8 to 12 items.
4. Run `python3 tools/live_build.py draft.json`. It checks speakers and lengths, makes the voice clips and rewrites `site/live/live.json`. If it errors, fix the draft and rerun. If ffmpeg is missing flite, `apt-get install -y ffmpeg` (or report it).
5. Check: `site/live/live.json` has the new `v`, the clip files exist, `git status` shows only `site/live/` changes.
6. Commit with message `live <v>` and push to `main`. If the push is rejected, `git pull --rebase` and push again. Never touch other files.
7. Reply with one line: what is now on air (the three headlines used). If news search is unavailable, still refresh the ticker and the rotating programme and say so.
