#!/bin/bash

for FILE in *.mp4; do
    echo -e "Processing video '\e[32m$FILE\e[0m'";
    ffmpeg -i "${FILE}" -c:v libx264 -preset slow -crf 22 -c:a copy "${FILE%.mp4}-converted.mp4";
done;
