import matplotlib.pyplot as plt
import statistics
import numpy as np
from datetime import datetime
import scipy.stats as st
import math
power = []
power_mean=[]
power_sd=[]
Cinterval=[]
CIN=[]
for p in range(1,11):
    power.append([])
    powerAllfile=[]
    for z in range(1,11):
        W,T = [],[]
        for line in open(f'C:\\data generator\\e-health result 10 samples\\locally\\weighted sum\\power\\power{p}-{z}.txt', "r"):
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
    power_mean.append(float("{:.3f}".format(statistics.mean(powerAllfile))))
    power_sd.append(float("{:.3f}".format(statistics.stdev(powerAllfile))))
    #calculate CI
    conf = st.t.interval(0.95, df=len(powerAllfile)-1, loc=np.mean(powerAllfile), scale=st.sem(powerAllfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    CIN.append(conf)
    CI = 2.262*(statistics.stdev(powerAllfile)/math.sqrt(len(powerAllfile)))
    Cinterval.append(CI)
    #print("%.2f %.2f"%(statistics.mean(cpuAllfile)-CI,statistics.mean(cpuAllfile)+CI))
print("Mean = %s \nSD = %s \nCinterval = %s"%(power_mean,power_sd,";".join(str(x) for x in CIN)))

power2 = []
power2_mean=[]
power2_sd=[]
C2interval=[]
CIN2=[]
for p in range(1,11):
    power2.append([])
    power2Allfile=[]
    for z in range(1,11):
        W,T = [],[]
        for line in open(f'C:\\data generator\\e-health result 10 samples\\locally\\fuzzy\\power\\power{p}-{z}.txt', "r"):
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
    power2_mean.append(float("{:.3f}".format(statistics.mean(power2Allfile))))
    power2_sd.append(float("{:.3f}".format(statistics.stdev(power2Allfile))))
    #calculate CI
    conf = st.t.interval(0.95, df=len(power2Allfile)-1, loc=np.mean(power2Allfile), scale=st.sem(power2Allfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    CIN2.append(conf)
    CI = 2.262*(statistics.stdev(power2Allfile)/math.sqrt(len(power2Allfile)))
    C2interval.append(CI)
    #print("%.2f %.2f"%(statistics.mean(cpuAllfile)-CI,statistics.mean(cpuAllfile)+CI))
print("Mean = %s \nSD = %s \nCinterval = %s"%(power2_mean,power2_sd,";".join(str(x) for x in CIN2)))

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('Total energy consumption spent by an end node')
ax.set_xlabel('Number of fog nodes')
ax.set_ylabel('Energy consumption (milliwatt-hour (mWh))')

plt.bar(r, power_mean, yerr=Cinterval, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='Weighted sum')
plt.bar(r + width, power2_mean, yerr=C2interval, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='Fuzzy logic')
plt.xticks(r + width/2,d)
plt.legend()
#plt.ylim((0,2))
plt.show()

