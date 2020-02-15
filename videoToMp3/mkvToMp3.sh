#!/bin/bash

for FILE in *.mkv; do
    echo -e "Processing video '\e[32m$FILE\e[0m'";
    ffmpeg -i "${FILE}" -c:a libmp3lame -q:a 4 "${FILE%.mkv}.mp3";
done;
