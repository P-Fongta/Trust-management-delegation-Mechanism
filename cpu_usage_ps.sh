#!/bin/bash

PNAME="$1"
LOG_FILE="$2"
PID=$(pidof ${PNAME})
cpuTime=$(top -b -n 1 -d 0.1 -p $PID | grep $PID | tail -1 | awk '{ print $11}')
memusage=$(smem -P $PNAME |grep $PID | awk '{print $8}')



FILENAME=/home/pi/aiocoap/DB/evidence.db
FILESIZE=$(stat --format=%s "$FILENAME")
FILENAME2=/home/pi/aiocoap/DB/trust.db
FILESIZE2=$(stat --format=%s "$FILENAME2")
total_size=$((FILESIZE+FILESIZE2))
echo "CPUTime: $cpuTime\tMEMusage: $memusage"
printf "%s\t%s\t%s\n" "$cpuTime $memusage $FILESIZE2" >> $LOG_FILE
SSHPASS='1' sshpass -e ssh pi@192.168.1.183 python power_measure.py

