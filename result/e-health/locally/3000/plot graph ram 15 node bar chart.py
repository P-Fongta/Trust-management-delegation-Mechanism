import matplotlib.pyplot as plt
import statistics
import numpy as np

ramfile01_max=[]
ramfile02_max=[]
ramfile03_max=[]


for z in range(1,16):
    ram1, ram2, ram3 = [],[],[]
    for line in open(f'C:\data generator\graph\\result 15 home appliances\\01\Do_locally_15trustee{z}.txt', 'r'):
        lines = [i for i in line.split()]
        ram1.append(int(lines[1])) 
    xv = max(ram1)
    ramfile01_max.append(xv)
print(ramfile01_max)

for z in range(1,16):
    ram1, ram2, ram3 = [],[],[]
    for line in open(f'C:\data generator\graph\\result 15 home appliances\\02\Do_locally_15trustee{z}.txt', 'r'):
        lines = [i for i in line.split()]
        ram2.append(int(lines[1])) 
    xv = max(ram2)
    ramfile02_max.append(xv)
print(ramfile02_max)

for z in range(1,16):
    ram1, ram2, ram3 = [],[],[]
    for line in open(f'C:\data generator\graph\\result 15 home appliances\\03\Do_locally_15trustee{z}.txt', 'r'):
        lines = [i for i in line.split()]
        ram3.append(int(lines[1])) 
    xv = max(ram3)
    ramfile03_max.append(xv)
print(ramfile03_max)
ram_mean=[]
ram_sd=[]
for z in range(0,15):
    k=[]
    k.append(ramfile01_max[z]/1024)
    k.append(ramfile02_max[z]/1024)
    k.append(ramfile03_max[z]/1024)
    ram_mean.append(float("{:.5f}".format(statistics.mean(k))))
    ram_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print(ram_mean)
print(ram_sd)
d = [i for i in range(1,16)]
fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('Ram usage of a home hub')
ax.set_xlabel('Number of home appliances (nodes)')
ax.set_ylabel('Ram usage (MB)')
ax.bar(d, ram_mean, yerr=ram_sd, align='center', alpha=0.8, color=['green'], capsize=10, width=0.5)
#ax.plot(d, cpu_mean, '-', color='tab:orange',label="Performing trust locally",linewidth=0.5)
# create a confidence band
#y_lower = [float(i) + float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#y_upper = [float(i) - float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')

ax.set_xticks(d)
ax.set_xticklabels(d)

#plt.legend(loc='upper right')

plt.ylim((0,70))
#plt.xlim((0,16))
plt.show()

