import matplotlib.pyplot as plt
import statistics
import numpy as np
import scipy.stats as st
import math
hdd = []
hdd_mean=[]
hdd_sd=[]
Cinterval=[]
for p in range(1,11):
    hdd.append([])
    hddAllfile=[]
    for z in range(1,11): 
        for line in open(f'C:\data generator\e-health result 10 samples\locally\\weighted sum\\result\\Do_locally{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                hddAllfile.append(int(lines[2])/1024) 
            except Exception:
                print('Line data error')
                #continue
    print(hddAllfile)
    hdd_mean.append(float("{:.3f}".format(statistics.mean(hddAllfile))))
    hdd_sd.append(float("{:.3f}".format(statistics.stdev(hddAllfile))))
    #calculate CI
    conf = st.t.interval(0.95, df=len(hddAllfile)-1, loc=np.mean(hddAllfile), scale=st.sem(hddAllfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))

    CI = 2.262*(statistics.stdev(hddAllfile)/math.sqrt(len(hddAllfile)))
    Cinterval.append(CI)
    #print("%.2f %.2f"%(statistics.mean(cpuAllfile)-CI,statistics.mean(cpuAllfile)+CI))
print("Mean = %s \nSD = %s \nCinterval = %s"%(hdd_mean,hdd_sd,";".join(str(x) for x in Cinterval)))


hdd2 = []
hdd2_mean=[]
hdd2_sd=[]
C2interval=[]
for p in range(1,11):
    hdd2.append([])
    hdd2Allfile=[]
    for z in range(1,11): 
        for line in open(f'C:\data generator\e-health result 10 samples\locally\\fuzzy\\result\\Do_locally{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                hdd2Allfile.append(int(lines[2])/1024) 
            except Exception:
                print('Line data error')
                #continue
    print(hdd2Allfile)
    hdd2_mean.append(float("{:.3f}".format(statistics.mean(hdd2Allfile))))
    hdd2_sd.append(float("{:.3f}".format(statistics.stdev(hdd2Allfile))))
    #calculate CI
    conf = st.t.interval(0.95, df=len(hdd2Allfile)-1, loc=np.mean(hdd2Allfile), scale=st.sem(hdd2Allfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))

    CI = 2.262*(statistics.stdev(hdd2Allfile)/math.sqrt(len(hdd2Allfile)))
    C2interval.append(CI)
    #print("%.2f %.2f"%(statistics.mean(cpuAllfile)-CI,statistics.mean(cpuAllfile)+CI))
print("Mean = %s \nSD = %s \nCinterval = %s"%(hdd2_mean,hdd2_sd,";".join(str(x) for x in C2interval)))


d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of HDD space used by an end node')
ax.set_xlabel('Number of fog nodes')
ax.set_ylabel('HDD usage (KB)')

plt.bar(r, hdd_mean, yerr=Cinterval, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='Weighted sum')
plt.bar(r + width, hdd2_mean, yerr=C2interval, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='Fuzzy logic')
plt.xticks(r + width/2,d)
plt.legend()
#plt.ylim((0,4.5))
plt.show()

