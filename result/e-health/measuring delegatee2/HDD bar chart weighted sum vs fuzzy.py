import matplotlib.pyplot as plt
import statistics
import numpy as np

hdd = []
for p in range(1,11):
    hdd.append([])
    for z in range(1,4):
        #i=0
        hddEachfile=[]
        
        for line in open(f'C:\\data generator\\e-health\\measuring delegatee\\delegatee collects evidence\\result\\server_delegation{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                hddEachfile.append(int(lines[2])) 
            except Exception:
                print('Line data error')
                #continue
        xv = max(hddEachfile)
        hdd[p-1].append(xv)
    print(hdd[p-1])

hdd2 = []
for p in range(1,11):
    hdd2.append([])
    for z in range(1,4):
        #i=0
        hdd2Eachfile=[]
        
        for line in open(f'C:\\data generator\\e-health\\measuring delegatee\\delegatee collects evidence\\result\\server_delegation{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                hdd2Eachfile.append(int(lines[2])) 
            except Exception:
                print('Line data error')
                #continue
        xv = max(hdd2Eachfile)
        hdd2[p-1].append(xv)
    print(hdd2[p-1])

hdd_mean=[]
hdd_sd=[]
for z in range(0,10):
    k=[]
    k.append(hdd[z][0]/1024/1024)
    k.append(hdd[z][1]/1024/1024)
    k.append(hdd[z][2]/1024/1024)
    hdd_mean.append(float("{:.5f}".format(statistics.mean(k))))
    hdd_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print("hdd Mean: %s"%hdd_mean)
print("hdd SD: %s"%hdd_sd)

hdd2_mean=[]
hdd2_sd=[]
for z in range(0,10):
    k=[]
    k.append(hdd2[z][0]/1024/1024)
    k.append(hdd2[z][1]/1024/1024)
    k.append(hdd2[z][2]/1024/1024)
    hdd2_mean.append(float("{:.5f}".format(statistics.mean(k))))
    hdd2_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print("hdd2 Mean: %s"%hdd2_mean)
print("hdd2 SD: %s"%hdd2_sd) 

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of HDD used by a medical sensor')
ax.set_xlabel('Number of fog nodes (Trustees)')
ax.set_ylabel('HDD usage (KB)')

plt.bar(r, hdd_mean, yerr=hdd_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='A delegate collects evidence')
plt.bar(r + width, hdd_mean, yerr=hdd2_sd, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='A medical sensor collects evidence itself')
plt.xticks(r + width/2,d)
plt.legend()
#plt.ylim((0,0.04))
plt.show()

