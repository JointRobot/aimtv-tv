#!/bin/bash
# AIMTV 24/7 YouTube stream: one-time server setup (Ubuntu 22.04/24.04, ARM or x86).
# Usage:  curl -fsSL https://raw.githubusercontent.com/JointRobot/aimtv-tv/main/setup.sh | sudo bash -s -- YOUR-YOUTUBE-STREAM-KEY
set -e
KEY="$1"; REPO="${AIMTV_REPO:-https://github.com/JointRobot/aimtv-tv.git}"
[ -z "$KEY" ] && { echo "Give the YouTube stream key: ... | sudo bash -s -- KEY"; exit 1; }
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get install -y -q curl xvfb pulseaudio ffmpeg git nodejs npm python3 fonts-noto-core fonts-noto-color-emoji
id aimtv >/dev/null 2>&1 || useradd -m -s /bin/bash aimtv
mkdir -p /opt/aimtv /etc/aimtv
echo "$KEY" > /etc/aimtv/key; chmod 600 /etc/aimtv/key; chown aimtv /etc/aimtv/key
[ -d /opt/aimtv/repo/.git ] || git clone --depth 1 "$REPO" /opt/aimtv/repo
export PLAYWRIGHT_BROWSERS_PATH=/opt/aimtv/browsers
npx -y playwright@1.47.2 install --with-deps chromium
cp /opt/aimtv/repo/stream.sh /opt/aimtv/repo/update.sh /opt/aimtv/; chmod +x /opt/aimtv/*.sh
chown -R aimtv /opt/aimtv
cat > /etc/systemd/system/aimtv.service <<U
[Unit]
Description=AIMTV live to YouTube
After=network-online.target
Wants=network-online.target
[Service]
User=aimtv
ExecStart=/opt/aimtv/stream.sh
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
U
cat > /etc/systemd/system/aimtv-update.service <<U
[Service]
Type=oneshot
User=aimtv
ExecStart=/opt/aimtv/update.sh
U
cat > /etc/systemd/system/aimtv-update.timer <<U
[Timer]
OnBootSec=2min
OnUnitActiveSec=5min
[Install]
WantedBy=timers.target
U
systemctl daemon-reload
systemctl enable --now aimtv.service aimtv-update.timer
echo "AIMTV is streaming. Check: systemctl status aimtv   |   logs: journalctl -u aimtv -f"
