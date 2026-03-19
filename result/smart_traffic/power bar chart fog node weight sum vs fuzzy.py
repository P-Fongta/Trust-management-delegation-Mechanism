import matplotlib.pyplot as plt
import statistics
import numpy as np
from datetime import datetime
import scipy.stats as st
power = []
power_mean=[]
power_sd=[]
Cinterval=[]
for p in range(1,11):
    power.append([])
    powerAllfile=[]
    for z in range(1,11):
        W,T = [],[]
        for line in open(f'C:\data generator\\smart_traffic\\fognode_towards_fog_end\\power_measure\\power{p}-{z}.txt', "r"):
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
for p in range(1,11):
    power2.append([])
    power2Allfile=[]
    for z in range(1,11):
        W,T = [],[]
        for line in open(f'C:\data generator\\smart_traffic\\fognode_towards_fog_end_fuzzy\\power_measure\\power{p}-{z}.txt', "r"):
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
print("Mean = %s \nSD = %s \nCinterval = %s"%(power2_mean,power2_sd,";".join(str(x) for x in C2interval)))


d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of energy used by a fog node to perform trust management')
ax.set_xlabel('Number of target end nodes and fog nodes (Trustees)')
ax.set_ylabel('Energy usage (mWh)')
plt.bar(r , power2_mean, yerr=power2_sd, color = 'tab:orange',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='fuzzy logic')
plt.bar(r+0.25, power_mean, yerr=power_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='weighted sum')
plt.xticks(r + width/2,d)
plt.legend()
#plt.ylim((0,2))
plt.show()

