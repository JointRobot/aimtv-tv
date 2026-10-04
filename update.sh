#!/bin/bash
# Every 5 minutes: fetch new songs/shows; if anything changed, reload the channel (a few seconds' gap).
cd /opt/aimtv/repo || exit 0
OLD=$(git rev-parse HEAD); git pull -q --ff-only || exit 0; NEW=$(git rev-parse HEAD)
[ "$OLD" != "$NEW" ] && pkill -f aimtv-profile || true
