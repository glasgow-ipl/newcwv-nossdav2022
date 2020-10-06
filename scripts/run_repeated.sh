#!/bin/bash
for i in 1 .. 10
do
	echo "Running experimet #$i"
	sudo python mn_script.py
	sleep 10
done
