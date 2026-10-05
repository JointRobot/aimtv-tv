#!/bin/bash
# Plays the AIMTV channel in a hidden screen and streams picture + sound to YouTube.
# AIMTV_OUT overrides the destination (for testing, e.g. a file path). AIMTV_NOAUDIO=1 uses silence.
SITE=/opt/aimtv/repo/site; [ -f /opt/aimtv/serve/index.html ] && SITE=/opt/aimtv/serve; [ -n "$AIMTV_SITE" ] && SITE="$AIMTV_SITE"
KEY=$(cat /etc/aimtv/key 2>/dev/null)
OUT="${AIMTV_OUT:-rtmp://a.rtmp.youtube.com/live2/$KEY}"
export DISPLAY=:99 XDG_RUNTIME_DIR=/tmp/aimtv-xdg; mkdir -p $XDG_RUNTIME_DIR; chmod 700 $XDG_RUNTIME_DIR
CHROME=$(ls -d ${PLAYWRIGHT_BROWSERS_PATH:-/opt/aimtv/browsers}/chromium-*/chrome-linux/chrome 2>/dev/null | tail -1)
pkill -u "$(id -u)" -f "Xvfb :99" 2>/dev/null; sleep 1
Xvfb :99 -screen 0 1280x720x24 -nolisten tcp & XPID=$!
if [ -z "$AIMTV_NOAUDIO" ]; then
  pulseaudio --kill 2>/dev/null; pulseaudio --start --exit-idle-time=-1
  pactl load-module module-null-sink sink_name=tv sink_properties=device.description=AIMTV >/dev/null
  pactl set-default-sink tv
  AIN=(-f pulse -thread_queue_size 1024 -i tv.monitor)
else AIN=(-f lavfi -i anullsrc=r=44100:cl=stereo); fi
python3 -m http.server 8417 --bind 127.0.0.1 --directory "$SITE" >/dev/null 2>&1 & HPID=$!
for i in $(seq 1 50); do curl -s --noproxy "*" -o /dev/null http://127.0.0.1:8417/index.html && break; sleep 0.2; done
# The channel: restarted automatically if it closes (the updater closes it to load new versions).
( while true; do
  "$CHROME" --no-sandbox --kiosk --window-size=1280,720 --window-position=0,0 \
    --autoplay-policy=no-user-gesture-required --no-first-run --disable-infobars --disable-gpu \
    --disable-features=Translate --user-data-dir=/tmp/aimtv-profile \
    "http://127.0.0.1:8417/index.html?broadcast=1" >/dev/null 2>&1
  sleep 2; done ) & CPID=$!
trap 'kill $CPID $HPID $XPID 2>/dev/null; pkill -f aimtv-profile; exit' INT TERM
sleep 6
FMT=flv; [[ "$OUT" != rtmp* ]] && FMT=mp4
exec ffmpeg -y -loglevel warning -f x11grab -draw_mouse 0 -framerate 30 -video_size 1280x720 -thread_queue_size 1024 -i :99 "${AIN[@]}" \
  -c:v libx264 -preset veryfast -tune zerolatency -b:v 3000k -maxrate 3000k -bufsize 6000k -g 60 -keyint_min 60 -pix_fmt yuv420p \
  -c:a aac -b:a 160k -ar 44100 ${AIMTV_SECONDS:+-t $AIMTV_SECONDS} -f $FMT "$OUT"
