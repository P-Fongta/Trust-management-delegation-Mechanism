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
    #print(lines[0])
    cpu1.append(lines[0])
    ram1.append(int(lines[1]))
    hdd1.append(int(lines[2]))

for line in open('C:\data generator\graph\\new_graph\locally\Do_locally2.txt', 'r'):
    lines = [i for i in line.split()]
    cpu2.append(lines[0])
    ram2.append(int(lines[1]))
    hdd2.append(int(lines[2]))
for line in open('C:\data generator\graph\\new_graph\locally\Do_locally3.txt', 'r'):
    lines = [i for i in line.split()]
    cpu3.append(lines[0])
    ram3.append(int(lines[1]))
    hdd3.append(int(lines[2]))
hdd_mean = [float("{:.2f}".format(statistics.mean(k)/1024/1024)) for k in zip(hdd1, hdd2,hdd3)]
hdd_sd = [float("{:.2f}".format(statistics.stdev(k)/1024/1024)) for k in zip(hdd1, hdd2,hdd3)]

for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation1.txt', 'r'):
    lines = [i for i in line.split()]
    dcpu1.append(lines[0])
    dram1.append(int(lines[1]))
    dhdd1.append(int(lines[2]))
for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation2.txt', 'r'):
    lines = [i for i in line.split()]
    dcpu2.append(lines[0])
    dram2.append(int(lines[1]))
    dhdd2.append(int(lines[2]))
for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation3.txt', 'r'):
    lines = [i for i in line.split()]
    dcpu3.append(lines[0])
    dram3.append(int(lines[1]))
    dhdd3.append(int(lines[2]))
dhdd_mean = [float("{:.2f}".format(statistics.mean(k)/1024/1024)) for k in zip(dhdd1, dhdd2,dhdd3)]
dhdd_sd = [float("{:.2f}".format(statistics.stdev(k)/1024/1024)) for k in zip(dhdd1, dhdd2,dhdd3)]

#calculate CI
Cinterval = [float("{:.3f}".format(4.303*(statistics.stdev(k)/math.sqrt(len(k))))) for k in zip(dhdd1, dhdd2,dhdd3)]
#print(Cinterval)

dCinterval = [float("{:.3f}".format(4.303*(statistics.stdev(k)/math.sqrt(len(k))))) for k in zip(dhdd1, dhdd2,dhdd3)]
#print(dCinterval)

#print mean SD CI locally
for x in range(1, len(hdd_mean),300):
    print(hdd_mean[x],  end=', ')
print("\n")
for x in range(1, len(hdd_sd),300):
    print(hdd_sd[x],  end=', ')
print("\n")
for x in range(1, len(Cinterval),300):
    #print(Cinterval[x],  end=', ')
    print("(%.2f, %.2f)"%(hdd_mean[x]-Cinterval[x],hdd_mean[x]+Cinterval[x]), end=';')
print("\n")

#print mean SD CI delegating
for x in range(1, len(dhdd_mean),300):
    print(dhdd_mean[x],  end=', ')
print("\n")
for x in range(1, len(dhdd_sd),300):
    print(dhdd_sd[x],  end=', ')
print("\n")
for x in range(1, len(Cinterval),300):
    #print(Cinterval[x],  end=', ')
    print("(%.2f, %.2f)"%(dhdd_mean[x]-dCinterval[x],dhdd_mean[x]+dCinterval[x]), end=';')
print("\n")

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
#ax.plot(d, ram1, '-', color='tab:orange')
#ax.plot(d, ram2, '-', color='tab:orange')
#ax.plot(d, ram3, '-', color='tab:orange')

ax.set_title('The amount of HDD space used by an end node')
ax.set_xlabel('The amount of evidence (Records)')
ax.set_ylabel('HDD Usage (MB)')

ax.plot(d, hdd_mean, '-', color='tab:orange',label="Performing trust locally")
# create a confidence band
y_lower = [float(i) + float(k)  for (i,k) in zip(hdd_mean,hdd_sd)]
y_upper = [float(i) - float(k)  for (i,k) in zip(hdd_mean,hdd_sd)]
ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')

ax.plot(d, dhdd_mean, '-', color='tab:green',label="Delegating trust")
# create a confidence band
dy_lower = [float(i) + float(k)  for (i,k) in zip(dhdd_mean,dhdd_sd)]
dy_upper = [float(i) - float(k)  for (i,k) in zip(dhdd_mean,dhdd_sd)]
ax.fill_between(d, dy_lower, dy_upper, alpha=0.1, color='tab:green')

plt.legend(loc='upper right')
#plt.ylim((18500,18900))
plt.xlim((0,3000))
plt.show()