#!/bin/bash
for ((p=1;p<=20;p++)); 
do
	for ((i=1;i<=10;i++)); 
	do
		
		sshpass -p '1' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null pi@192.168.1.106 "tmux new -d -s s1; tmux send-keys 'python /home/pi/aiocoap/smart_traffic/power_measure/power_measure.py $p $i' Enter"
		#tmux new -d -s s2; tmux send-keys -t s2 'bash /home/pi/aiocoap/e-health/cpu2.sh' Enter
		sudo python run_trust_locally_fuzzy.py $p $p
		sshpass -p '1' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null pi@192.168.1.106 "tmux kill-ses -t s1"
		#tmux kill-ses -t s2
		#sleep 1
		
		sudo cp -r /home/pi/aiocoap/smart_traffic/DBcopy/* /home/pi/aiocoap/smart_traffic/DB/
		
		#cp /home/pi/aiocoap/e-health/cpulog.txt /home/pi/aiocoap/e-health/cpulog/
		#rm -rf /home/pi/aiocoap/e-health/cpulog.txt
		#mv /home/pi/aiocoap/e-health/cpulog/cpulog.txt /home/pi/aiocoap/e-health/cpulog/cpulog$p-$i.txt
		sleep 5
		
		
	done
	cp /home/pi/aiocoap/smart_traffic/locally/Do_locally.txt /home/pi/aiocoap/smart_traffic/locally/result/
	rm -rf /home/pi/aiocoap/smart_traffic/locally/Do_locally.txt
	mv /home/pi/aiocoap/smart_traffic/locally/result/Do_locally.txt /home/pi/aiocoap/smart_traffic/locally/result/Do_locally$p.txt
done