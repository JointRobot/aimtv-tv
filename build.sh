#!/bin/bash
# Builds the broadcast site (what the server plays) from the receiver.
set -e; cd "$(dirname "$0")"; OUT=site; rm -rf $OUT; mkdir -p $OUT/music $OUT/vo
{ echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'; cat ../aimtv.html; echo '</html>'; } > $OUT/index.html
cp ../music/*.mp3 $OUT/music/ 2>/dev/null || true
[ -d ../vo ] && cp -r ../vo/. $OUT/vo/ || true
date -u +%FT%TZ > $OUT/VERSION
