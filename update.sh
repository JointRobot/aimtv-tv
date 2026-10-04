#!/bin/bash
# Every 5 minutes: fetch new songs/shows. The live news folder (site/live) is picked up by the page itself, no restart.
# Only restart the channel (a few seconds' gap) when the player, songs or voices changed.
cd /opt/aimtv/repo || exit 0
OLD=$(git rev-parse HEAD); git pull -q --ff-only || exit 0; NEW=$(git rev-parse HEAD)
if [ "$OLD" != "$NEW" ] && git diff --name-only "$OLD" "$NEW" | grep '^site/' | grep -qv '^site/live/'; then pkill -f aimtv-profile || true; fi
