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
        for line in open(f'C:\\data generator\\e-health result 10 samples\\measuring delegatee2\\vary the number of delegatees\\power\\power{p}-{z}.txt', "r"):
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
    conf = st.t.interval(0.95, len(powerAllfile)-1, loc=np.mean(powerAllfile), scale=st.sem(powerAllfile)) 
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
        for line in open(f'C:\data generator\e-health result 10 samples\measuring delegatee2\\vary the number of delegators\\power\\power{p}-{z}.txt', "r"):
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
    conf2 = st.t.interval(0.95, len(power2Allfile)-1, loc=np.mean(power2Allfile), scale=st.sem(power2Allfile)) 
    conf2 = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf2))
    C2interval.append(conf2)
    power2_mean.append(float("{:.3f}".format(statistics.mean(power2Allfile))))
    power2_sd.append(float("{:.3f}".format(statistics.stdev(power2Allfile))))
print("Mean = %s \nSD = %s \nCinterval = %s "%(power2_mean,power2_sd,";".join(str(x) for x in C2interval)))

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of energy used by a delegate')
ax.set_xlabel('Number of trustees/trustors')
ax.set_ylabel('Energy usage (milliWatt-hour (mWh))')

plt.bar(r, power_mean, yerr=power_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='varying the number of trustees')
plt.bar(r + width, power2_mean, yerr=power2_sd, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='varying the number of trustors')
plt.xticks(r + width/2,d)
plt.legend()
plt.ylim((20,55))
plt.show()

