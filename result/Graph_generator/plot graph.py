import matplotlib.pyplot as plt
import statistics
import numpy as np
cpu1, cpu2, cpu3 = [],[],[]
ram1,ram2 ,ram3 = [],[],[]
hdd1,hdd2 ,hdd3 = [],[],[]
dcpu1, dcpu2, dcpu3 = [],[],[]
dram1,dram2 ,dram3 = [],[],[]
dhdd1,dhdd2 ,dhdd3 = [],[],[]
d = [i for i in range(1,1000)]

for line in open('C:\data generator\graph\locally\Do_locally.txt', 'r'):
    lines = [i for i in line.split()]
    cpu1.append(lines[0])
    ram1.append(int(lines[1]))
    hdd1.append(int(lines[2]))
for line in open('C:\data generator\graph\locally\Do_locally2.txt', 'r'):
    lines = [i for i in line.split()]
    cpu2.append(lines[0])
    ram2.append(int(lines[1]))
    hdd2.append(int(lines[2]))
for line in open('C:\data generator\graph\locally\Do_locally3.txt', 'r'):
    lines = [i for i in line.split()]
    cpu3.append(lines[0])
    ram3.append(int(lines[1]))
    hdd3.append(int(lines[2]))
ram_mean = [float("{:.2f}".format(statistics.mean(k))) for k in zip(ram1, ram2,ram3)]
ram_sd = [float("{:.2f}".format(statistics.stdev(k))) for k in zip(ram1, ram2,ram3)]
hdd_mean = [float("{:.2f}".format(statistics.mean(k))) for k in zip(hdd1, hdd2,hdd3)]
hdd_sd = [float("{:.2f}".format(statistics.stdev(k))) for k in zip(hdd1, hdd2,hdd3)]

for line in open('C:\data generator\graph\delegation\Do_delegation.txt', 'r'):
    lines = [i for i in line.split()]
    dcpu1.append(lines[0])
    dram1.append(int(lines[1]))
    dhdd1.append(int(lines[2]))
for line in open('C:\data generator\graph\delegation\Do_delegation2.txt', 'r'):
    lines = [i for i in line.split()]
    dcpu2.append(lines[0])
    dram2.append(int(lines[1]))
    dhdd2.append(int(lines[2]))
for line in open('C:\data generator\graph\delegation\Do_delegation3.txt', 'r'):
    lines = [i for i in line.split()]
    dcpu3.append(lines[0])
    dram3.append(int(lines[1]))
    dhdd3.append(int(lines[2]))
dram_mean = [float("{:.2f}".format(statistics.mean(k))) for k in zip(dram1, dram2,dram3)]
dram_sd = [float("{:.2f}".format(statistics.stdev(k))) for k in zip(dram1, dram2,dram3)]
dhdd_mean = [float("{:.2f}".format(statistics.mean(k))) for k in zip(dhdd1, dhdd2,dhdd3)]
dhdd_sd = [float("{:.2f}".format(statistics.stdev(k))) for k in zip(dhdd1, dhdd2,dhdd3)]

fig, host = plt.subplots(figsize=(12,8), layout='constrained')




color1, color2 = plt.cm.viridis([0, .5])

p1 = host.plot(d, ram_mean, '-', color=color1 ,label="Performing trust locally")
# create a confidence band
#y_lower = [float(i) + float(k)  for (i,k) in zip(ram_mean,ram_sd)]
#y_upper = [float(i) - float(k)  for (i,k) in zip(ram_mean,ram_sd)]
#ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')
ax2 = host.twinx()
p2 = ax2.plot(d, dram_mean, '-', color=color2 ,label="Delegating trust")
# create a confidence band
#dy_lower = [float(i) + float(k)  for (i,k) in zip(dram_mean,dram_sd)]
#dy_upper = [float(i) - float(k)  for (i,k) in zip(dram_mean,dram_sd)]
#ax.fill_between(d, dy_lower, dy_upper, alpha=0.1, color='tab:green')
host.set_title('Ram Usage')
host.set_xlabel('Iteration')
host.set_ylabel('RAM Usage (KB)')
ax2.set_ylabel("RAM Usage (KB)")
#plt.legend(loc='upper right')
host.legend(handles=p1+p2, loc='best')
host.yaxis.label.set_color(p1[0].get_color())
ax2.yaxis.label.set_color(p2[0].get_color())
plt.ylim((18500,18900))
plt.show()