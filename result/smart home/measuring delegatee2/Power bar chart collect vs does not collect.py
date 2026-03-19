import matplotlib.pyplot as plt
import statistics
import numpy as np
from datetime import datetime
power = []
power_mean=[]
power_sd=[]
for p in range(1,11):
    power.append([])
    powerAllfile=[]
    for z in range(1,11):
        W,T = [],[]
        for line in open(f'C:\data generator\e-health result 10 samples\measuring delegatee\delegatee does not collect evidence\\power\\power{p}-{z}.txt', "r"):
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
        powerAllfile.append(Energy)
    print(powerAllfile)
    power_mean.append(float("{:.5f}".format(statistics.mean(powerAllfile))))
    power_sd.append(float("{:.5f}".format(statistics.stdev(powerAllfile))))
print("Mean = %s \nSD = %s "%(power_mean,power_sd))

power2 = []
power2_mean=[]
power2_sd=[]
for p in range(1,11):
    power2.append([])
    power2Allfile=[]
    for z in range(1,11):
        W,T = [],[]
        for line in open(f'C:\data generator\e-health result 10 samples\measuring delegatee\delegatee collects evidence\\power\\power{p}-{z}.txt', "r"):
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
        power2Allfile.append(Energy)
    print(power2Allfile)
    power2_mean.append(float("{:.5f}".format(statistics.mean(power2Allfile))))
    power2_sd.append(float("{:.5f}".format(statistics.stdev(power2Allfile))))
print("Mean = %s \nSD = %s "%(power2_mean,power2_sd))

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of energy used by a delegate')
ax.set_xlabel('Number of end nodes (Delegators)')
ax.set_ylabel('Energy usage (milliWatt-hour (mWh))')

plt.bar(r, power_mean, yerr=power_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='A delegate does not collect evidence')
plt.bar(r + width, power2_mean, yerr=power2_sd, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='A delegate collects evidence')
plt.xticks(r + width/2,d)
plt.legend()
#plt.ylim((0,2))
plt.show()

