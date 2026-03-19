import matplotlib.pyplot as plt
import statistics
import numpy as np
from datetime import datetime
power = []
for p in range(1,11):
    power.append([])
    for z in range(1,4):
        #i=0
        powerEachfile=[]
        W,T = [],[]
        for line in open(f'C:\\data generator\\e-health\\measuring delegatee\\delegatee does not collect evidence\\power_measure\\power{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                W.append(float(lines[2])) 
                T.append(str(lines[3]))

            except Exception:
                print('Line data error')
                #continue
        dt_objstart = datetime.strptime(T[0], "%H:%M:%S")
        dt_objend = datetime.strptime(T[len(T)-1], "%H:%M:%S")
        timediff = dt_objend  - dt_objstart
        Energy = float("{:.5f}".format(statistics.mean(W))) * (timediff.seconds/3600)
        powerEachfile.append(Energy)
        xv = powerEachfile
        power[p-1].append(Energy)
    print(power[p-1])
    
power2 = []
for p in range(1,11):
    power2.append([])
    for z in range(1,4):
        #i=0
        power2Eachfile=[]
        W,T = [],[]
        for line in open(f'C:\\data generator\\e-health\\measuring delegatee\\delegatee collects evidence\\power_measure\\power{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                W.append(float(lines[2])) 
                T.append(str(lines[3]))

            except Exception:
                print('Line data error')
                #continue
        dt_objstart = datetime.strptime(T[0], "%H:%M:%S")
        dt_objend = datetime.strptime(T[len(T)-1], "%H:%M:%S")
        timediff = dt_objend  - dt_objstart
        Energy = float("{:.5f}".format(statistics.mean(W))) * (timediff.seconds/3600)
        power2Eachfile.append(Energy)
        xv = power2Eachfile
        power2[p-1].append(Energy)
    print(power2[p-1])

power_mean=[]
power_sd=[]
for z in range(0,10):
    k=[]
    k.append(power[z][0]/1000)
    k.append(power[z][1]/1000)
    k.append(power[z][2]/1000)
    power_mean.append(float("{:.5f}".format(statistics.mean(k))))
    power_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print("power Mean: %s"%power_mean)
print("power SD: %s"%power_sd)

power2_mean=[]
power2_sd=[]
for z in range(0,10):
    k=[]
    k.append(power2[z][0]/1000)
    k.append(power2[z][1]/1000)
    #k.append(power2[z][2]/1000)
    power2_mean.append(float("{:.5f}".format(statistics.mean(k))))
    power2_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print("power2 Mean: %s"%power2_mean)
print("power2 SD: %s"%power2_sd) 

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of energy used by a medical sensor')
ax.set_xlabel('Number of fog nodes (Trustees)')
ax.set_ylabel('Energy usage (Watt-hour (Wh))')

plt.bar(r, power_mean, yerr=power_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='A delegate does not collect evidence')
plt.bar(r + width, power2_mean, yerr=power2_sd, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='A delegate collects evidence')
plt.xticks(r + width/2,d)
plt.legend()
#plt.ylim((0,30))
plt.show()

