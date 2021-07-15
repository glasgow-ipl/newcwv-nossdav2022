#!/bin/sh

if [ $# != 2 ]; then
  echo "Usage: $0 <url> <outputfile>"
  exit 1
fi

if [ -f $2 ]; then
  echo "download $1 -> $2 (if changed)";
  curl -L --progress-bar -o $2 -z $2 $1;
else
  echo "download $1 -> $2";
  curl -L --progress-bar -o $2       $1;
fi

