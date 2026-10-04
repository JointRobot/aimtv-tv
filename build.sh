#!/bin/bash
# Builds the broadcast site (what the server plays) from the receiver.
set -e; cd "$(dirname "$0")"; OUT=site; mkdir -p $OUT; find $OUT -mindepth 1 -maxdepth 1 ! -name live -exec rm -rf {} +; mkdir -p $OUT/music $OUT/vo $OUT/live  # site/live is written by the hourly live refresh: never wipe it
{ echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'; cat ../aimtv.html; echo '</html>'; } > $OUT/index.html
cp ../music/*.mp3 $OUT/music/ 2>/dev/null || true
[ -d ../plates ] && mkdir -p $OUT/plates && cp ../plates/*.jpg $OUT/plates/ || true  # comic-art backdrops
[ -d ../vo ] && cp -r ../vo/. $OUT/vo/ || true
date -u +%FT%TZ > $OUT/VERSION
