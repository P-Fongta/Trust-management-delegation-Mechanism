import matplotlib.pyplot as plt
import statistics
import numpy as np
from datetime import datetime
Energy_file01=[]
Energy_file02=[]
Energy_file03=[]



for z in range(1,16):
    W,T = [],[]
    for line in open(f'C:\data generator\graph\\result 15 home appliances\\01\power{z}.txt', 'r'):
        lines = [i for i in line.split()]
        W.append(float(lines[2])) 
        T.append(str(lines[3]))
    dt_objstart = datetime.strptime(T[0], "%H:%M:%S")
    dt_objend = datetime.strptime(T[len(T)-1], "%H:%M:%S")
    timediff = dt_objend  - dt_objstart
    Energy = float("{:.5f}".format(statistics.mean(W))) * (timediff.seconds/3600)
    Energy_file01.append(Energy)
    #print("%f %s"%(Energy, timediff))

for z in range(1,16):
    W,T = [],[]
  
    for line in open(f'C:\data generator\graph\\result 15 home appliances\\02\power{z}.txt', 'r'):
        lines = [i for i in line.split()]
        W.append(float(lines[2])) 
        T.append(str(lines[3]))
        #print(str(lines[3]))
     
    dt_objstart = datetime.strptime(T[0], "%H:%M:%S")
    
    dt_objend = datetime.strptime(T[len(T)-1], "%H:%M:%S")
    #print(dt_objstart)
    #print(dt_objend)
    timediff = dt_objend  - dt_objstart
    Energy = float("{:.5f}".format(statistics.mean(W))) * (timediff.seconds/3600)
    Energy_file02.append(Energy)

for z in range(1,16):
    W,T = [],[]
    for line in open(f'C:\\data generator\\graph\\result 15 home appliances\\03\power{z}.txt', 'r'):
        lines = [i for i in line.split()]
        W.append(float(lines[2])) 
        T.append(str(lines[3]))
    dt_objstart = datetime.strptime(T[0], "%H:%M:%S")
    dt_objend = datetime.strptime(T[len(T)-1], "%H:%M:%S")
    timediff = dt_objend  - dt_objstart
    Energy = float("{:.5f}".format(statistics.mean(W))) * (timediff.seconds/3600)
    Energy_file03.append(Energy)

print(Energy_file01)
print(Energy_file02)
print(Energy_file03)

Energy_mean=[]
Energy_sd=[]
for z in range(0,15):
    k=[]
    k.append(Energy_file01[z]/1000)
    k.append(Energy_file02[z]/1000)
    k.append(Energy_file03[z]/1000)
    Energy_mean.append(float("{:.5f}".format(statistics.mean(k))))
    Energy_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print(Energy_mean)
print(Energy_sd)

d = [i for i in range(1,16)]
fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('Total energy usage of a homehub')
ax.set_xlabel('Number of home appliances (nodes)')
ax.set_ylabel('Energy usage (Wh)')
ax.bar(d, Energy_mean, yerr=Energy_sd, align='center', alpha=0.8, color=['green'], capsize=10, width=0.5)
#ax.plot(d, cpu_mean, '-', color='tab:orange',label="Performing trust locally",linewidth=0.5)
# create a confidence band
#y_lower = [float(i) + float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#y_upper = [float(i) - float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')

ax.set_xticks(d)
ax.set_xticklabels(d)

#plt.legend(loc='upper right')

plt.ylim((0,10))
#plt.xlim((0,9))
plt.show()


