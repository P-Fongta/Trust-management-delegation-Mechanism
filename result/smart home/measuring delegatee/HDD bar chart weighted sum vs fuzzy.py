import matplotlib.pyplot as plt
import statistics
import numpy as np
import scipy.stats as st
import math
hdd = []
hdd_mean=[]
hdd_sd=[]
CIN=[]
for p in range(1,11):
    hdd.append([])
    hddAllfile=[]
    for z in range(1,11): 
        for line in open(f'C:\data generator\e-health result 10 samples\measuring delegatee\delegatee collects evidence\\result\\server_delegation{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                hddAllfile.append(int(lines[2])/1024) 
            except Exception:
                print('Line data error')
                #continue
    print(hddAllfile)
    hdd_mean.append(float("{:.5f}".format(statistics.mean(hddAllfile))))
    hdd_sd.append(float("{:.5f}".format(statistics.stdev(hddAllfile))))
print("Mean = %s \nSD = %s "%(hdd_mean,hdd_sd))

hdd2 = []
hdd2_mean=[]
hdd2_sd=[]
CIN=[]
for p in range(1,11):
    hdd2.append([])
    hdd2Allfile=[]
    for z in range(1,11): 
        for line in open(f'C:\data generator\e-health result 10 samples\measuring delegatee\\fuzzy delegatee collects evidence\\result\\server_delegation{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                hdd2Allfile.append(int(lines[2])/1024) 
            except Exception:
                print('Line data error')
                #continue
    print(hdd2Allfile)
    hdd2_mean.append(float("{:.5f}".format(statistics.mean(hdd2Allfile))))
    hdd2_sd.append(float("{:.5f}".format(statistics.stdev(hdd2Allfile))))
print("Mean = %s \nSD = %s "%(hdd2_mean,hdd2_sd))

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of HDD space used by a delegate')
ax.set_xlabel('Number of end nodes')
ax.set_ylabel('HDD usage (KB)')

plt.bar(r, hdd_mean, yerr=hdd_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='Weighted sum')
plt.bar(r + width, hdd2_mean, yerr=hdd2_sd, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='Fuzzy logic')
plt.xticks(r + width/2,d)
plt.legend()
#plt.ylim((0,180))
plt.show()

