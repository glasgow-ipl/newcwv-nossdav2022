#!/bin/sh

if [ $# = 0 ]; then
 echo "usage: bin/check-for-todo.sh <file> ..."
 exit 1
fi
 
for i in $*
do
  # Find instances of \todo{} that are not commented out:
  egrep -H -i -n "\\\\todo\\{" $i | egrep -v ".*%.*\\\\todo" | egrep --color "\\\\todo" || true

  # Find instances of FIXME:
  egrep -H -i -n --color "FIXME" $i || true
done

