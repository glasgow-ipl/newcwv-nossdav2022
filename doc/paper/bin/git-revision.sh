#!/bin/sh

if [ $# -ne 1 ]; then
  echo "Usage: git-revision.sh <outputfile>"
  exit 1
fi

REV=`git rev-parse --verify HEAD`

git diff --no-ext-diff --quiet --exit-code
if [ $? -eq 1 ]; then
  MOD="++"
else
  MOD=""
fi

NEWREV=$REV$MOD

if [ ! -f $1 ]; then
  echo "Created $1"
  echo $NEWREV > $1
else 
  OLDREV=`cat $1`
  if [ $OLDREV != $NEWREV ]; then
    echo "Updated $1"
    echo $NEWREV > $1
  fi
fi

