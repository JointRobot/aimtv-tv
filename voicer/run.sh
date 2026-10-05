#!/bin/bash
# Runs neural.py at low priority, one at a time. Called by update.sh after each fetch.
exec 9>/tmp/aimtv-voicer.lock; flock -n 9 || exit 0
nice -n 19 /opt/aimtv/tts/bin/python /opt/aimtv/repo/voicer/neural.py >> /tmp/aimtv-voicer.log 2>&1
