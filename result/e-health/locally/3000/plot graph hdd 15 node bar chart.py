import matplotlib.pyplot as plt
import statistics
import numpy as np

hddfile01_max=[]
hddfile02_max=[]
hddfile03_max=[]


for z in range(1,16):
    hdd1, hdd2, hdd3 = [],[],[]
    for line in open(f'C:\data generator\graph\\result 15 home appliances\\01\Do_locally_15trustee{z}.txt', 'r'):
        lines = [i for i in line.split()]
        hdd1.append(int(lines[2])) 
    xv = max(hdd1)
    hddfile01_max.append(xv)
print(hddfile01_max)

for z in range(1,16):
    hdd1, hdd2, hdd3 = [],[],[]
    for line in open(f'C:\data generator\graph\\result 15 home appliances\\02\Do_locally_15trustee{z}.txt', 'r'):
        lines = [i for i in line.split()]
        hdd1.append(int(lines[2])) 
    xv = max(hdd1)
    hddfile02_max.append(xv)
print(hddfile02_max)

for z in range(1,16):
    hdd1, hdd2, hdd3 = [],[],[]
    for line in open(f'C:\data generator\graph\\result 15 home appliances\\03\Do_locally_15trustee{z}.txt', 'r'):
        lines = [i for i in line.split()]
        hdd1.append(int(lines[2])) 
    xv = max(hdd1)
    hddfile03_max.append(xv)
print(hddfile03_max)
hdd_mean=[]
hdd_sd=[]
for z in range(0,15):
    k=[]
    k.append(hddfile01_max[z]/1024/1024)
    k.append(hddfile02_max[z]/1024/1024)
    k.append(hddfile03_max[z]/1024/1024)
    hdd_mean.append(float("{:.5f}".format(statistics.mean(k))))
    hdd_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print(hdd_mean)
print(hdd_sd)

d = [i for i in range(1,16)]
fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('HDD usage of a home hub')
ax.set_xlabel('Number of home appliances (nodes)')
ax.set_ylabel('HDD usage (MB)')
ax.bar(d, hdd_mean, yerr=hdd_sd, align='center', alpha=0.8, color=['green'], capsize=10, width=0.5)
#ax.plot(d, cpu_mean, '-', color='tab:orange',label="Performing trust locally",linewidth=0.5)
# create a confidence band
#y_lower = [float(i) + float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#y_upper = [float(i) - float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')

ax.set_xticks(d)
ax.set_xticklabels(d)

#plt.legend(loc='upper right')

plt.ylim((0,7))
#plt.xlim((0,16))
plt.show()

