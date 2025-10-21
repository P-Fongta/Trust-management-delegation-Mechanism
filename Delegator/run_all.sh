#!/bin/bash
for ((p=1;p<=10;p++)); 
do
	for ((i=1;i<=3;i++)); 
	do
		
		sshpass -p '1' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null pi@192.168.1.105 "tmux new -d -s s1; tmux send-keys 'python /home/pi/aiocoap/e-health/power_measure/power_measure.py $p $i' Enter"
		tmux new -d -s s2; tmux send-keys -t s2 'bash /home/pi/aiocoap/e-health/cpu2.sh' Enter
		sudo python D_all_client_multiple_trustee.py $p
		sleep 1
		while [ 1 ]
		do
			 cnt=`ps x | grep -v grep | grep -c D_all_client_multiple_trustee.py`
			 if  [ $cnt -eq 0 ]
			 then
				break
			 fi
			 sleep 5
		done
		cp /home/pi/aiocoap/e-health/delegation/Do_delegation.txt /home/pi/aiocoap/e-health/delegation/result/
		rm -rf /home/pi/aiocoap/e-health/delegation/Do_delegation.txt
		mv /home/pi/aiocoap/e-health/delegation/result/Do_delegation.txt /home/pi/aiocoap/e-health/delegation/result/Do_delegation$p-$i.txt
		sudo cp -r /home/pi/aiocoap/e-health/DBcopy/* /home/pi/aiocoap/e-health/DB/
		tmux kill-ses -t s2
		cp /home/pi/aiocoap/e-health/cpulog.txt /home/pi/aiocoap/e-health/cpulog/
		rm -rf /home/pi/aiocoap/e-health/cpulog.txt
		mv /home/pi/aiocoap/e-health/cpulog/cpulog.txt /home/pi/aiocoap/e-health/cpulog/cpulog$p-$i.txt
		
		sshpass -p '1' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null pi@192.168.1.105 "tmux kill-ses -t s1"
		
		
	done
done