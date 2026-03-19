import matplotlib.pyplot as plt
import statistics
import numpy as np
import scipy.stats as st
hdd = []
hdd_mean=[]
hdd_sd=[]
Cinterval=[]
for p in range(1,11):
    hdd.append([])
    hddAllfile=[]
    for z in range(1,11): 
        for line in open(f'C:\\data generator\\e-health result 10 samples\\measuring endnode vs fog node\\measuring end node\\result\\Do_locally{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                hddAllfile.append(int(lines[2])/1024) 
            except Exception:
                print('Line data error')
                #continue
    print(hddAllfile)
    conf = st.t.interval(0.95, len(hddAllfile)-1, loc=np.mean(hddAllfile), scale=st.sem(hddAllfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    Cinterval.append(conf)
    hdd_mean.append(float("{:.5f}".format(statistics.mean(hddAllfile))))
    hdd_sd.append(float("{:.5f}".format(statistics.stdev(hddAllfile))))
print("Mean = %s \nSD = %s \nCinterval = %s"%(hdd_mean,hdd_sd,";".join(str(x) for x in Cinterval)))

hdd2 = []
hdd2_mean=[]
hdd2_sd=[]
C2interval=[]
for p in range(1,11):
    hdd2.append([])
    hdd2Allfile=[]
    for z in range(1,11): 
        for line in open(f'C:\\data generator\\e-health result 10 samples\\measuring endnode vs fog node\\measuring fog node\\result\\Do_locally{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                hdd2Allfile.append(int(lines[2])/1024) 
            except Exception:
                print('Line data error')
                #continue
    print(hdd2Allfile)
    conf2 = st.t.interval(0.95, len(hdd2Allfile)-1, loc=np.mean(hdd2Allfile), scale=st.sem(hdd2Allfile)) 
    conf2 = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf2))
    C2interval.append(conf2)
    hdd2_mean.append(float("{:.5f}".format(statistics.mean(hdd2Allfile))))
    hdd2_sd.append(float("{:.5f}".format(statistics.stdev(hdd2Allfile))))
print("Mean = %s \nSD = %s \nCinterval = %s "%(hdd2_mean,hdd2_sd,";".join(str(x) for x in C2interval)))

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of HDD space used by a fog node')
ax.set_xlabel('Number of end nodes/ fog nodes')
ax.set_ylabel('HDD usage (KB)')

plt.bar(r, hdd_mean, yerr=hdd_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='Evaluating end nodes')
plt.bar(r + width, hdd_mean, yerr=hdd_sd, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='Evaluating fog nodes')
plt.xticks(r + width/2,d)
plt.legend()
plt.ylim((20,100))
plt.show()

