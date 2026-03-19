import matplotlib.pyplot as plt
import statistics
import numpy as np
import math
cpu1, cpu2, cpu3 = [],[],[]
dcpu1, dcpu2, dcpu3 = [],[],[]


minus_cpu1, minus_cpu2, minus_cpu3 = [],[],[]
minus_dcpu1, minus_dcpu2, minus_dcpu3 = [],[],[]
d = [i for i in range(1,3000)]

for line in open('C:\data generator\graph\\new_graph\locally\Do_locally1.txt', 'r'):
    lines = [i for i in line.split()]
    
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = cpu_p23[0]
    cpu_p3 = cpu_p23[1]
    second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100)  
    #print(str((second)))
    cpu1.append(second)


for line in open('C:\data generator\graph\\new_graph\locally\Do_locally2.txt', 'r'):
    lines = [i for i in line.split()]
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = cpu_p23[0]
    cpu_p3 = cpu_p23[1]
    second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100)  
    #print(str((second)))
    cpu2.append(second)

for line in open('C:\data generator\graph\\new_graph\locally\Do_locally3.txt', 'r'):
    lines = [i for i in line.split()]
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = cpu_p23[0]
    cpu_p3 = cpu_p23[1]
    second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100)  
    #print(str((second)))
    cpu3.append(second)


for x in range(1, len(cpu1)):
    minus_cpu1.append(float(cpu1[x])-float(cpu1[x-1]))
#print(str((minus_cpu1)))
for x in range(1, len(cpu2)):
    minus_cpu2.append(float(cpu2[x])-float(cpu2[x-1]))

for x in range(1, len(cpu3)):
    minus_cpu3.append(float(cpu3[x])-float(cpu3[x-1]))


cpu_mean = [float("{:.3f}".format(statistics.mean(k))) for k in zip(minus_cpu1, minus_cpu2,minus_cpu3)]

cpu_sd = [float("{:.3f}".format(statistics.stdev(k))) for k in zip(minus_cpu1, minus_cpu2,minus_cpu3)]

#print(str((cpu_mean)))

for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation1.txt', 'r'):
    lines = [i for i in line.split()]
    #print(lines)
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = cpu_p23[0]
    cpu_p3 = cpu_p23[1]
    second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100)  
    #print(str((second)))
    dcpu1.append(second)

for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation2.txt', 'r'):
    lines = [i for i in line.split()]
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = cpu_p23[0]
    cpu_p3 = cpu_p23[1]
    second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100) 
    dcpu2.append(second)

for line in open('C:\data generator\graph\\new_graph\delegation\Do_delegation3.txt', 'r'):
    lines = [i for i in line.split()]
    cpu_p1 = lines[0].split(":")[0]
    cpu_p23 = lines[0].split(":")[1].split(".")
    cpu_p2 = cpu_p23[0]
    cpu_p3 = cpu_p23[1]
    second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100) 
    dcpu3.append(second)

for x in range(1, len(dcpu1)):
    minus_dcpu1.append(float(dcpu1[x])-float(dcpu1[x-1]))

for x in range(1, len(dcpu2)):
    minus_dcpu2.append(float(dcpu2[x])-float(dcpu2[x-1]))

for x in range(1, len(dcpu3)):
    minus_dcpu3.append(float(dcpu3[x])-float(dcpu3[x-1]))


dcpu_mean = [float("{:.3f}".format(statistics.mean(k))) for k in zip(minus_dcpu1, minus_dcpu2,minus_dcpu3)]
dcpu_sd = [float("{:.3f}".format(statistics.stdev(k))) for k in zip(minus_dcpu1, minus_dcpu2,minus_dcpu3)]


#calculate CI
Cinterval = [float("{:.3f}".format(4.303*(statistics.stdev(k)/math.sqrt(len(k))))) for k in zip(minus_cpu1, minus_cpu2,minus_cpu3)]
#print(Cinterval)

dCinterval = [float("{:.3f}".format(4.303*(statistics.stdev(k)/math.sqrt(len(k))))) for k in zip(minus_dcpu1, minus_dcpu2,minus_dcpu3)]
#print(dCinterval)

#print mean SD CI locally
for x in range(1, len(cpu_mean),300):
    print(cpu_mean[x],  end=', ')
print("\n")
for x in range(1, len(cpu_sd),300):
    print(cpu_sd[x],  end=', ')
print("\n")
for x in range(1, len(Cinterval),300):
    #print(Cinterval[x],  end=', ')
    print("(%.2f, %.2f)"%(cpu_mean[x]-Cinterval[x],cpu_mean[x]+Cinterval[x]), end=';')
print("\n")

#print mean SD CI delegating
for x in range(1, len(dcpu_mean),300):
    print(dcpu_mean[x],  end=', ')
print("\n")
for x in range(1, len(dcpu_sd),300):
    print(dcpu_sd[x],  end=', ')
print("\n")
for x in range(1, len(Cinterval),300):
    #print(Cinterval[x],  end=', ')
    print("(%.2f, %.2f)"%(dcpu_mean[x]-dCinterval[x],dcpu_mean[x]+dCinterval[x]), end=';')
print("\n")

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('CPU Time used by an end node')
ax.set_xlabel('The amount of evidence (Records)')
ax.set_ylabel('CPU Time (Seconds)')

ax.plot(d, cpu_mean, '-', color='tab:orange',label="Performing trust locally",linewidth=0.5)
# create a confidence band
y_lower = [float(i) + float(k)  for (i,k) in zip(cpu_mean,Cinterval)]
y_upper = [float(i) - float(k)  for (i,k) in zip(cpu_mean,Cinterval)]
ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')

ax.plot(d, dcpu_mean, '-', color='tab:green',label="Delegating trust", linewidth=0.5)
# create a confidence band
dy_lower = [float(i) + float(k)  for (i,k) in zip(dcpu_mean,dCinterval)]
dy_upper = [float(i) - float(k)  for (i,k) in zip(dcpu_mean,dCinterval)]
ax.fill_between(d, dy_lower, dy_upper, alpha=0.1, color='tab:green')

#print(cpu_sd)
#print(dcpu_sd)
plt.legend(loc='upper right')
#plt.ylim((18000,21000))
plt.ylim((0,0.4))
plt.xlim((0,3000))
plt.show()
