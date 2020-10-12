#!/bin/bash

deps=('ffmpeg' 'python' 'mn' 'firefox')

for d in "${deps[@]}"
do
    echo "Checking dependency ${d}"
    printf "Dependency ${d} is "
    test=`which ${d}`
    if [ -z "$test" ]; then
        echo "NOT satisfied"
        exit 1
    else
        echo "satisfied"
    fi
    echo ""
done