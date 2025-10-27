#!/bin/sh
# chmod a+x m4aToWav.sh

for f in *.m4a *.M4A; do
  [ -e "$f" ] || continue
  ffmpeg -hide_banner -loglevel error -i "$f" -ac 1 -ar 16000 -c:a pcm_s16le "${f%.*}.wav"
done
