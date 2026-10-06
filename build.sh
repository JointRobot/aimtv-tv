#!/bin/bash
# Builds the broadcast site (what the server plays) from the receiver.
set -e; cd "$(dirname "$0")"; OUT=site; mkdir -p $OUT; find $OUT -mindepth 1 -maxdepth 1 ! -name live -exec rm -rf {} +; mkdir -p $OUT/music $OUT/vo $OUT/live  # site/live is written by the hourly live refresh: never wipe it
{ echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'; cat ../aimtv.html; echo '</html>'; } > $OUT/index.html
cp ../music/*.mp3 $OUT/music/ 2>/dev/null || true
[ -d ../plates ] && mkdir -p $OUT/plates && cp ../plates/*.jpg $OUT/plates/ || true  # comic-art backdrops
[ -d ../vo ] && cp -r ../vo/. $OUT/vo/ || true
cp ../brand/og.jpg $OUT/og.jpg 2>/dev/null || true  # link-preview picture
[ -d ../brand/yt ] && mkdir -p $OUT/yt && cp ../brand/yt/*.jpg $OUT/yt/ || true  # YouTube channel art
date -u +%FT%TZ > $OUT/VERSION
printf "/live/*\n  Cache-Control: no-store\n/music/*\n  Cache-Control: public, max-age=604800\n/vo/*\n  Cache-Control: public, max-age=86400\n/index.html\n  Cache-Control: no-cache\n" > $OUT/_headers  # Cloudflare Pages caching rules
