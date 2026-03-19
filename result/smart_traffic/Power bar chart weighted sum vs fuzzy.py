import matplotlib.pyplot as plt
import statistics
import numpy as np
from datetime import datetime
import scipy.stats as st
import scipy.stats as st
import math
power = []
power_mean=[]
power_sd=[]
Cinterval=[]
for p in range(1,11):
    power.append([])
    powerAllfile=[]
    for z in range(1,11):
        W,T = [],[]
        for line in open(f'C:\data generator\\smart_traffic\\locally\\power_measure\\power{p}-{z}.txt', "r"):
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
    conf = st.t.interval(0.95, df=len(powerAllfile)-1, loc=np.mean(powerAllfile), scale=st.sem(powerAllfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    Cinterval.append(conf)
    power_mean.append(float("{:.3f}".format(statistics.mean(powerAllfile))))
    power_sd.append(float("{:.3f}".format(statistics.stdev(powerAllfile))))
print("Mean = %s \nSD = %s \nCinterval = %s"%(power_mean,power_sd,";".join(str(x) for x in Cinterval)))

power2 = []
power2_mean=[]
power2_sd=[]
C2interval=[]
CI2 = []
for p in range(1,11):
    power2.append([])
    power2Allfile=[]
    for z in range(1,11):
        W,T = [],[]
        for line in open(f'C:\data generator\\smart_traffic\\delegation\\power_measure\\power{p}-{z}.txt', "r"):
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
    conf = st.t.interval(0.95, df=len(power2Allfile)-1, loc=np.mean(power2Allfile), scale=st.sem(power2Allfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    C2interval.append(conf)
    power2_mean.append(float("{:.3f}".format(statistics.mean(power2Allfile))))
    power2_sd.append(float("{:.3f}".format(statistics.stdev(power2Allfile))))

    CI2.append(2.262*(statistics.stdev(power2Allfile)/math.sqrt(len(power2Allfile))))
print("Mean = %s \nSD = %s \nCinterval = %s"%(power2_mean,power2_sd,";".join(str(x) for x in C2interval)))

power3 = []
power3_mean=[]
power3_sd=[]
C3interval=[]
CI3 = []
for p in range(1,11):
    power3.append([])
    powerAllfile=[]
    for z in range(1,11):
        W,T = [],[]
        for line in open(f'C:\data generator\\smart_traffic\\fuzzy\\power_measure\\power{p}-{z}.txt', "r"):
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
    conf = st.t.interval(0.95, df=len(powerAllfile)-1, loc=np.mean(powerAllfile), scale=st.sem(powerAllfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    C3interval.append(conf)
    power3_mean.append(float("{:.3f}".format(statistics.mean(powerAllfile))))
    power3_sd.append(float("{:.3f}".format(statistics.stdev(powerAllfile))))

    CI3.append(2.262*(statistics.stdev(powerAllfile)/math.sqrt(len(powerAllfile))))
print("Mean3 = %s \nSD = %s \nCinterval = %s"%(power3_mean,power3_sd,";".join(str(x) for x in C3interval)))

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of energy spent by an end node')
ax.set_xlabel('Number of target end nodes and fog nodes')
ax.set_ylabel('Energy usage (mWh)')
plt.bar(r , power3_mean, yerr=CI3, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='Performing trust locally (fuzzy logic)')
#plt.bar(r+0.25, power_mean, yerr=power_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
#        width = width, edgecolor = 'black',
#        label='Performing trust locally (weighted sum)')
plt.bar(r + 0.25, power2_mean, yerr=CI2, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='Delegating trust')
plt.xticks(r + width/2,d)
plt.legend()
#plt.ylim((0,2))
plt.show()

