#!/bin/sh
# chmod a+x mp4ToWav.sh

for f in *.mp4; do
  [ -e "$f" ] || continue
  ffmpeg -hide_banner -loglevel error -i "$f" -vn -ac 1 -ar 16000 -c:a pcm_s16le "${f%.*}.wav"
done
