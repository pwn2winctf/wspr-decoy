#!/bin/bash -xe
cd recordings
for file in *.raw; do
    sox -t raw -r 12000 -b 16 -c 1 -L -e signed-integer "$file" "$(basename "$file" .raw)".wav
done
