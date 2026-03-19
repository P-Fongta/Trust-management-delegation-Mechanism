import matplotlib.pyplot as plt
import statistics
import numpy as np
cpu = []
for p in range(1,11):
    cpu.append([])
    for z in range(1,4):
        #i=0
        cpuEachfile=[]
        
        for line in open(f'C:\\data generator\\e-health\\measuring delegatee\\delegatee does not collect evidence\\result\\server_delegation{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                cpu_p1 = lines[0].split(":")[0]
                cpu_p23 = lines[0].split(":")[1].split(".")
                cpu_p2 = cpu_p23[0]
                cpu_p3 = cpu_p23[1]
                second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100)  
                #print(str((second)))
                cpuEachfile.append(second)
                #print("%s %s %d"%(p,z,i))
                #i=i+1
            except Exception:
                print('Line data error')
                #continue
        xv = max(cpuEachfile)
        cpu[p-1].append(xv)
    print(cpu[p-1])

cpu2 = []
for p in range(1,11):
    cpu2.append([])
    for z in range(1,4):
        #i=0
        cpuEachfile=[]
        
        for line in open(f'C:\\data generator\\e-health\\measuring delegatee\\delegatee collects evidence\\result\\server_delegation{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                cpu_p1 = lines[0].split(":")[0]
                cpu_p23 = lines[0].split(":")[1].split(".")
                cpu_p2 = cpu_p23[0]
                cpu_p3 = cpu_p23[1]
                second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100)  
                #print(str((second)))
                cpuEachfile.append(second)
                #print("%s %s %d"%(p,z,i))
                #i=i+1
            except Exception:
                print('Line data error')
                #continue
        xv = max(cpuEachfile)
        cpu2[p-1].append(xv)
    print(cpu2[p-1])
"""
minus_cpu = []
for x in range(1, len(cpu)):
    minus_cpu.append(float(cpu[x])-float(cpu[x-1]))
print(str((minus_cpu)))
"""
cpu_mean=[]
cpu_sd=[]
for z in range(0,10):
    k=[]
    k.append(cpu[z][0])
    k.append(cpu[z][1])
    k.append(cpu[z][2])
    cpu_mean.append(float("{:.5f}".format(statistics.mean(k))))
    cpu_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print("CPU Mean: %s"%cpu_mean)
print("CPU SD: %s"%cpu_sd)

cpu2_mean=[]
cpu2_sd=[]
for z in range(0,10):
    k=[]
    k.append(cpu2[z][0])
    k.append(cpu2[z][1])
    k.append(cpu2[z][2])
    cpu2_mean.append(float("{:.5f}".format(statistics.mean(k))))
    cpu2_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print("CPU2 Mean: %s"%cpu2_mean)
print("CPU2 SD: %s"%cpu2_sd)


d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('CPU Time of a medical sensor')
ax.set_xlabel('Number of fog nodes (Trustees)')
ax.set_ylabel('CPU Time (Seconds)')

plt.bar(r, cpu_mean, yerr=cpu_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='A delegate does not collect evidence')
plt.bar(r + width, cpu2_mean, yerr=cpu2_sd, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='A delegate collects evidence')
plt.xticks(r + width/2,d)
plt.legend()
#ax.bar(d, cpu_mean, yerr=cpu_sd, align='center', alpha=0.8, color=['green'], capsize=10, width=0.5)
#ax.plot(d, cpu_mean, '-', color='tab:orange',label="Performing trust locally",linewidth=0.5)
# create a confidence band
#y_lower = [float(i) + float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#y_upper = [float(i) - float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')

#ax.set_xticks(d)
#ax.set_xticklabels(d)

#plt.legend(loc='upper right')

#plt.ylim((0,1000))
#plt.xlim((0,16))
plt.show()

