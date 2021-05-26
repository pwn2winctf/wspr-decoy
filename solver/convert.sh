#!/bin/bash -xe
for file in recordings/*.raw; do
    sox -t raw -r 12000 -b 16 -c 1 -L -e signed-integer "$file" "$(basename "$file")".wav
done
