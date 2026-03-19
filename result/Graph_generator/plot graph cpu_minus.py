import matplotlib.pyplot as plt
import statistics
import numpy as np
cpu1, cpu2, cpu3 = [],[],[]
dcpu1, dcpu2, dcpu3 = [],[],[]


minus_cpu1, minus_cpu2, minus_cpu3 = [],[],[]
minus_dcpu1, minus_dcpu2, minus_dcpu3 = [],[],[]
d = [i for i in range(1,3000)]

for line in open('C:\data generator\graph\\new_graph\locally\Do_locally1.txt', 'r'):
    lines = [i for i in line.split()]
    
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = lines[0].split(":")[1].split(".")[0]
    cpu_p3 = lines[0].split(":")[1].split(".")[1]
    cpu_p23=float(cpu_p2)+(float(cpu_p3)/100)
    cpu_p23=cpu_p23/60
    cpu1_total=float(cpu_p1)+cpu_p23
    #print(str((cpu_total)))
    cpu1.append(cpu1_total)


for line in open('C:\data generator\graph\\new_graph\locally\Do_locally2.txt', 'r'):
    lines = [i for i in line.split()]
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = lines[0].split(":")[1].split(".")[0]
    cpu_p3 = lines[0].split(":")[1].split(".")[1]
    cpu_p23=float(cpu_p2)+(float(cpu_p3)/100)
    cpu_p23=cpu_p23/60
    cpu2_total=float(cpu_p1)+cpu_p23
    cpu2.append(cpu2_total)

for line in open('C:\data generator\graph\\new_graph\locally\Do_locally3.txt', 'r'):
    lines = [i for i in line.split()]
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = lines[0].split(":")[1].split(".")[0]
    cpu_p3 = lines[0].split(":")[1].split(".")[1]
    cpu_p23=float(cpu_p2)+(float(cpu_p3)/100)
    cpu_p23=cpu_p23/60
    cpu3_total=float(cpu_p1)+cpu_p23
    cpu3.append(cpu3_total)


for x in range(1, len(cpu1)):
    minus_cpu1.append(float(cpu1[x])-float(cpu1[x-1]))
print(minus_cpu1)
for x in range(1, len(cpu2)):
    minus_cpu2.append(float(cpu2[x])-float(cpu2[x-1]))
print(minus_cpu2)
for x in range(1, len(cpu3)):
    minus_cpu3.append(float(cpu3[x])-float(cpu3[x-1]))
print(minus_cpu3)

cpu_mean = [float("{:.5f}".format(statistics.mean(k))) for k in zip(minus_cpu1, minus_cpu2,minus_cpu3)]
cpu_sd = [float("{:.5f}".format(statistics.stdev(k))) for k in zip(minus_cpu1, minus_cpu2,minus_cpu3)]

for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation1.txt', 'r'):
    lines = [i for i in line.split()]
    #print(lines)
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = lines[0].split(":")[1].split(".")[0]
    cpu_p3 = lines[0].split(":")[1].split(".")[1]
    cpu_p23=float(cpu_p2)+(float(cpu_p3)/100)
    cpu_p23=cpu_p23/60
    dcpu1_total=float(cpu_p1)+cpu_p23
    dcpu1.append(dcpu1_total)

for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation2.txt', 'r'):
    lines = [i for i in line.split()]
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = lines[0].split(":")[1].split(".")[0]
    cpu_p3 = lines[0].split(":")[1].split(".")[1]
    cpu_p23=float(cpu_p2)+(float(cpu_p3)/100)
    cpu_p23=cpu_p23/60
    dcpu2_total=float(cpu_p1)+cpu_p23
    dcpu2.append(dcpu2_total)

for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation3.txt', 'r'):
    lines = [i for i in line.split()]
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = lines[0].split(":")[1].split(".")[0]
    cpu_p3 = lines[0].split(":")[1].split(".")[1]
    cpu_p23=float(cpu_p2)+(float(cpu_p3)/100)
    cpu_p23=cpu_p23/60
    dcpu3_total=float(cpu_p1)+cpu_p23
    dcpu3.append(dcpu3_total)

for x in range(1, len(dcpu1)):
    minus_dcpu1.append(float(dcpu1[x])-float(dcpu1[x-1]))
print(minus_dcpu1)
for x in range(1, len(dcpu2)):
    minus_dcpu2.append(float(dcpu2[x])-float(dcpu2[x-1]))
print(minus_dcpu2)
for x in range(1, len(dcpu3)):
    minus_dcpu3.append(float(dcpu3[x])-float(dcpu3[x-1]))
print(minus_dcpu3)

dcpu_mean = [float("{:.5f}".format(statistics.mean(k))) for k in zip(minus_dcpu1, minus_dcpu2,minus_dcpu3)]
dcpu_sd = [float("{:.5f}".format(statistics.stdev(k))) for k in zip(minus_dcpu1, minus_dcpu2,minus_dcpu3)]

"""
local = [i for i in ram_mean[0::99]]
delegate = [i for i in dram_mean[0::99]]
print(local)
print(delegate)

#ax.plot(d, ram1, '-', color='tab:orange')
#ax.plot(d, ram2, '-', color='tab:orange')
#ax.plot(d, ram3, '-', color='tab:orange')
"""
fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('CPU Time')
ax.set_xlabel('Amount of Evidence (Records)')
ax.set_ylabel('CPU Time (Minutes)')

ax.plot(d, cpu_mean, '-', color='tab:orange',label="Performing trust locally")
# create a confidence band
y_lower = [float(i) + float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
y_upper = [float(i) - float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')

ax.plot(d, dcpu_mean, '-', color='tab:green',label="Delegating trust")
# create a confidence band
dy_lower = [float(i) + float(k)  for (i,k) in zip(dcpu_mean,dcpu_sd)]
dy_upper = [float(i) - float(k)  for (i,k) in zip(dcpu_mean,dcpu_sd)]
ax.fill_between(d, dy_lower, dy_upper, alpha=0.1, color='tab:green')
print(cpu_sd)
#print(dcpu_sd)
plt.legend(loc='upper right')
#plt.ylim((18000,21000))
plt.ylim((0,0.01))
#plt.xlim((0,1000))
plt.show()
