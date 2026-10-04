# AIMTV — 24/7 live stream to YouTube

This repo is what the AIMTV stream server plays. `site/` is the channel (receiver + songs + voices).
Push a new `site/` and the server picks it up within 5 minutes.

Server setup (once, on a fresh Ubuntu server):

    curl -fsSL https://raw.githubusercontent.com/JointRobot/aimtv-tv/main/setup.sh | sudo bash -s -- YOUR-STREAM-KEY

Check it: `systemctl status aimtv` · logs: `journalctl -u aimtv -f`
