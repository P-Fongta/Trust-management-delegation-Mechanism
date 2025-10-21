#!/bin/bash

PNAME="python"
LOG_FILE="Do_locally.txt"
PID=$(pidof ${PNAME})
cpuTime=$(top -b -n 1 -d 0.1 -p $PID | grep $PID | tail -1 | awk '{ print $11, $6}')
elapsedTime=$(ps -p $PID -o etimes= )


FILENAME=/home/pi/aiocoap/e-health/DB/evidence.db
FILESIZE=$(stat --format=%s "$FILENAME")
FILENAME2=/home/pi/aiocoap/e-health/DB/trust.db
FILESIZE2=$(stat --format=%s "$FILENAME2")
total_size=$((FILESIZE+FILESIZE2))
echo "CPUTime: $cpuTime elapsedTime: $elapsedTime"
printf "%s\t%s\t%s\t%s\n" "$cpuTime $total_size $(date +'%T') $elapsedTime" >> $LOG_FILE
#SSHPASS='1' sshpass -e ssh pi@192.168.1.108 python power_measure.py

