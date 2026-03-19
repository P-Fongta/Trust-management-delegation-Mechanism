import matplotlib.pyplot as plt
import statistics
import numpy as np
cpu = []

for p in range(1,9):
    cpu.append([])
    for z in range(1,4):
        cpuEachfile=[]
        for line in open(f'C:\\data generator\\e-health\locally\\3000\\fuzzy logic\\result\\Do_locally{p}-{z}.txt', "r"):
            lines = [i for i in line.split()]
            cpu_p1 = lines[0].split(":")[0]
            cpu_p23 = lines[0].split(":")[1].split(".")
            cpu_p2 = cpu_p23[0]
            cpu_p3 = cpu_p23[1]
            second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100)  
            #print(str((second)))
            cpuEachfile.append(second)
        xv = max(cpuEachfile)
        cpu[p-1].append(xv)
    print(cpu[p-1])

cpu_mean=[]
cpu_sd=[]
for z in range(0,8):
    k=[]
    k.append(cpu[z][0])
    k.append(cpu[z][1])
    k.append(cpu[z][2])
    cpu_mean.append(float("{:.5f}".format(statistics.mean(k))))
    cpu_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print(cpu_mean)
print(cpu_sd)


d = [i for i in range(1,9)]
fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('CPU Time of a medical sensor')
ax.set_xlabel('Number of fog nodes (nodes)')
ax.set_ylabel('CPU Time (Seconds)')

ax.bar(d, cpu_mean, yerr=cpu_sd, align='center', alpha=0.8, color=['green'], capsize=10, width=0.5)
#ax.plot(d, cpu_mean, '-', color='tab:orange',label="Performing trust locally",linewidth=0.5)
# create a confidence band
#y_lower = [float(i) + float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#y_upper = [float(i) - float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')

ax.set_xticks(d)
ax.set_xticklabels(d)

#plt.legend(loc='upper right')

#plt.ylim((0,1000))
#plt.xlim((0,16))
plt.show()

