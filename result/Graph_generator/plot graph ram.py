import matplotlib.pyplot as plt
import statistics
import numpy as np
import math
cpu1, cpu2, cpu3 = [],[],[]
ram1,ram2 ,ram3 = [],[],[]
hdd1,hdd2 ,hdd3 = [],[],[]
dcpu1, dcpu2, dcpu3 = [],[],[]
dram1,dram2 ,dram3 = [],[],[]
dhdd1,dhdd2 ,dhdd3 = [],[],[]
d = [i for i in range(1,3001)]

for line in open('C:\data generator\graph\\new_graph\locally\Do_locally1.txt', 'r'):
    lines = [i for i in line.split()]
    cpu1.append(lines[0])
    ram1.append(int(lines[1])/1000)
    hdd1.append(int(lines[2]))
for line in open('C:\data generator\graph\\new_graph\locally\Do_locally2.txt', 'r'):
    lines = [i for i in line.split()]
    cpu2.append(lines[0])
    ram2.append(int(lines[1])/1000)
    hdd2.append(int(lines[2]))
for line in open('C:\data generator\graph\\new_graph\locally\Do_locally3.txt', 'r'):
    lines = [i for i in line.split()]
    cpu3.append(lines[0])
    ram3.append(int(lines[1])/1000)
    hdd3.append(int(lines[2]))
ram_mean = [float("{:.3f}".format(statistics.mean(k))) for k in zip(ram1, ram2,ram3)]
ram_sd = [float("{:.3f}".format(statistics.stdev(k))) for k in zip(ram1, ram2,ram3)]
hdd_mean = [float("{:.3f}".format(statistics.mean(k))) for k in zip(hdd1, hdd2,hdd3)]
hdd_sd = [float("{:.3f}".format(statistics.stdev(k))) for k in zip(hdd1, hdd2,hdd3)]

for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation1.txt', 'r'):
    lines = [i for i in line.split()]
    dcpu1.append(lines[0])
    dram1.append(int(lines[1])/1000)
    dhdd1.append(int(lines[2]))
for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation2.txt', 'r'):
    lines = [i for i in line.split()]
    dcpu2.append(lines[0])
    dram2.append(int(lines[1])/1000)
    dhdd2.append(int(lines[2]))
for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation3.txt', 'r'):
    lines = [i for i in line.split()]
    dcpu3.append(lines[0])
    dram3.append(int(lines[1])/1000)
    dhdd3.append(int(lines[2]))
dram_mean = [float("{:.3f}".format(statistics.mean(k))) for k in zip(dram1, dram2,dram3)]
dram_sd = [float("{:.3f}".format(statistics.stdev(k))) for k in zip(dram1, dram2,dram3)]
dhdd_mean = [float("{:.3f}".format(statistics.mean(k))) for k in zip(dhdd1, dhdd2,dhdd3)]
dhdd_sd = [float("{:.3f}".format(statistics.stdev(k))) for k in zip(dhdd1, dhdd2,dhdd3)]


#calculate CI
Cinterval = [float("{:.3f}".format(4.303*(statistics.stdev(k)/math.sqrt(len(k))))) for k in zip(ram1, ram2,ram3)]
#print(Cinterval)

dCinterval = [float("{:.3f}".format(4.303*(statistics.stdev(k)/math.sqrt(len(k))))) for k in zip(dram1, dram2,dram3)]
#print(dCinterval)

#print mean SD CI locally
for x in range(1, len(ram_mean),300):
    print(ram_mean[x],  end=', ')
print("\n")
for x in range(1, len(ram_sd),300):
    print(ram_sd[x],  end=', ')
print("\n")
for x in range(1, len(Cinterval),300):
    #print(Cinterval[x],  end=', ')
    print("(%.2f, %.2f)"%(ram_mean[x]-Cinterval[x],ram_mean[x]+Cinterval[x]), end=';')
print("\n")

#print mean SD CI delegating
for x in range(1, len(dram_mean),300):
    print(dram_mean[x],  end=', ')
print("\n")
for x in range(1, len(dram_sd),300):
    print(dram_sd[x],  end=', ')
print("\n")
for x in range(1, len(Cinterval),300):
    #print(Cinterval[x],  end=', ')
    print("(%.2f, %.2f)"%(dram_mean[x]-dCinterval[x],dram_mean[x]+dCinterval[x]), end=';')
print("\n")

fig, ax = plt.subplots(figsize=(12, 8)) 

#ax.plot(d, ram1, '-', color='tab:orange')
#ax.plot(d, ram2, '-', color='tab:orange')
#ax.plot(d, ram3, '-', color='tab:orange')

ax.set_title('The amount of RAM used by an end node')
ax.set_xlabel('The amount of evidence (Records)')
ax.set_ylabel('RAM Usage (MB)')

twin1 = ax.twinx()

p1,=ax.plot(d, ram_mean, '-', color='tab:orange',label="Performing trust locally")
# create a confidence band
y_lower = [float(i) + float(k)  for (i,k) in zip(ram_mean,Cinterval)]
y_upper = [float(i) - float(k)  for (i,k) in zip(ram_mean,Cinterval)]
ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')

p2,=twin1.plot(d, dram_mean, '-', color='tab:green',label="Delegating trust")
# create a confidence band
dy_lower = [float(i) + float(k)  for (i,k) in zip(dram_mean,dCinterval)]
dy_upper = [float(i) - float(k)  for (i,k) in zip(dram_mean,dCinterval)]
twin1.fill_between(d, dy_lower, dy_upper, alpha=0.1, color='tab:green')
twin1.set_ylabel("RAM Usage (MB)")
ax.yaxis.label.set_color(p1.get_color())
twin1.yaxis.label.set_color(p2.get_color())
tkw = dict(size=4, width=1.5)
ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
ax.tick_params(axis='x', **tkw)
#plt.legend(loc='upper right')
ax.legend(handles=[p1, p2])
ax.set_xlim(0, 3000)
ax.set_ylim(14, 18)
twin1.set_ylim(17, 21)

plt.show()