#!/bin/bash

for FILE in *.mp4; do
    echo -e "Processing video '\e[32m$FILE\e[0m'";
    ffmpeg -i "${FILE}" -f mp3 -ab 192000 -vn "${FILE%.mp4}.mp3";
done;
