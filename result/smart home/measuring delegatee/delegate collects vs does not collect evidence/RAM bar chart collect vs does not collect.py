import matplotlib.pyplot as plt
import statistics
import numpy as np
import scipy.stats as st
import math
ram = []
ram_mean=[]
ram_sd=[]
Cinterval=[]
CIN=[]
for p in range(1,11):
    ram.append([])
    ramAllfile=[]
    for z in range(1,11):
        for line in open(f'C:\data generator\e-health result 10 samples\measuring delegatee\delegatee does not collect evidence\\result\\server_delegation{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                ramAllfile.append(int(lines[1])/1024) 
            except Exception:
                print('Line data error')
                #continue
    print(ramAllfile)
    ram_mean.append(float("{:.5f}".format(statistics.mean(ramAllfile))))
    ram_sd.append(float("{:.5f}".format(statistics.stdev(ramAllfile))))
    #calculate CI
    conf = st.t.interval(0.95, df=len(ramAllfile)-1, loc=np.mean(ramAllfile), scale=st.sem(ramAllfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    CIN.append(conf)
    CI = 2.262*(statistics.stdev(ramAllfile)/math.sqrt(len(ramAllfile)))
    Cinterval.append(CI)
    #print("%.2f %.2f"%(statistics.mean(cpuAllfile)-CI,statistics.mean(cpuAllfile)+CI))
print("Mean = %s \nSD = %s \nCinterval = %s"%(ram_mean,ram_sd,";".join(str(x) for x in CIN)))

ram2 = []
ram2_mean=[]
ram2_sd=[]
C2interval=[]
CIN2=[]
for p in range(1,11):
    ram2.append([])
    ram2Allfile=[]
    for z in range(1,11):
        for line in open(f'C:\data generator\e-health result 10 samples\measuring delegatee\delegatee collects evidence\\result\\server_delegation{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                ram2Allfile.append(int(lines[1])/1024) 
            except Exception:
                print('Line data error')
                #continue
    print(ram2Allfile)
    ram2_mean.append(float("{:.5f}".format(statistics.mean(ram2Allfile))))
    ram2_sd.append(float("{:.5f}".format(statistics.stdev(ram2Allfile))))
    #calculate CI
    conf = st.t.interval(0.95, df=len(ram2Allfile)-1, loc=np.mean(ram2Allfile), scale=st.sem(ram2Allfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    CIN2.append(conf)
    CI = 2.262*(statistics.stdev(ram2Allfile)/math.sqrt(len(ram2Allfile)))
    C2interval.append(CI)
    #print("%.2f %.2f"%(statistics.mean(cpuAllfile)-CI,statistics.mean(cpuAllfile)+CI))
print("Mean = %s \nSD = %s \nCinterval = %s"%(ram2_mean,ram2_sd,";".join(str(x) for x in CIN2)))

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of RAM used by a delegate')
ax.set_xlabel('Number of end nodes')
ax.set_ylabel('RAM usage (MB)')

plt.bar(r, ram_mean, yerr=Cinterval, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='A delegate does not collect evidence')
plt.bar(r + width, ram2_mean, yerr=C2interval, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='A delegate collects evidence')
plt.xticks(r + width/2,d)
plt.legend()
plt.ylim((0,30))
plt.show()

