import matplotlib.pyplot as plt
import statistics
import numpy as np
import scipy.stats as st
import seaborn as sns
import scipy.stats as st
import math
mean=[]
sd=[]
CI = []
Cinterval=[]
for p in range(1,11):
    ram = []
    for line in open(f'C:\data generator\\smart_traffic\\locally\\result\\Do_locally{p}.txt', "r"):
        try:
            lines = [i for i in line.split()]
            ram.append(int(lines[1])/1024)
        except Exception:
            print('Line data error')
            #continue
    print(ram)
    conf = st.t.interval(0.95, df=len(ram)-1, loc=np.mean(ram), scale=st.sem(ram)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    Cinterval.append(conf)
    conf_int = 1.96 * statistics.stdev(ram) / np.sqrt(len(ram))
    mean.append(float("{:.3f}".format(statistics.mean(ram))))
    sd.append(float("{:.3f}".format(statistics.stdev(ram))))

    CI.append(2.262*(statistics.stdev(ram)/math.sqrt(len(ram))))
print("Mean = %s \nSD = %s \nCinterval = %s"%(mean,sd,";".join(str(x) for x in Cinterval)))

mean2=[]
sd2=[]
C2interval=[]
CI2 = []
for p in range(1,11):
    ram = []
    for line in open(f'C:\data generator\\smart_traffic\\delegation\\result\\Do_delegation{p}.txt', "r"):
        try:
            lines = [i for i in line.split()]
            ram.append(int(lines[1])/1024)
        except Exception:
            print('Line data error')
            #continue
    print(ram)
    conf = st.t.interval(0.95, df=len(ram)-1, loc=np.mean(ram), scale=st.sem(ram)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 3) or x, conf))
    C2interval.append(conf)
    conf_int = 1.96 * statistics.stdev(ram) / np.sqrt(len(ram))
    mean2.append(float("{:.2f}".format(statistics.mean(ram))))
    sd2.append(float("{:.2f}".format(statistics.stdev(ram))))

    CI2.append(2.262*(statistics.stdev(ram)/math.sqrt(len(ram))))
print("Mean2 = %s \nSD2 = %s \nCinterval = %s"%(mean2,sd2,";".join(str(x) for x in C2interval)))

mean3=[]
sd3=[]
C3interval=[]
CI3 = []
for p in range(1,11):
    ram = []
    for line in open(f'C:\data generator\\smart_traffic\\fuzzy\\result\\Do_locally{p}.txt', "r"):
        try:
            lines = [i for i in line.split()]
            ram.append(int(lines[1])/1024)
        except Exception:
            print('Line data error')
            #continue
    print(ram)
    conf = st.t.interval(0.95, df=len(ram)-1, loc=np.mean(ram), scale=st.sem(ram)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    C3interval.append(conf)
    mean3.append(float("{:.3f}".format(statistics.mean(ram))))
    sd3.append(float("{:.3f}".format(statistics.stdev(ram))))

    CI3.append(2.262*(statistics.stdev(ram)/math.sqrt(len(ram))))
print("Mean3 = %s \nSD = %s \nCinterval = %s"%(mean3,sd3,";".join(str(x) for x in C3interval)))


d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of RAM used by an end node')
ax.set_xlabel('Number of target end nodes and fog nodes')
ax.set_ylabel('RAM usage (MB)')

plt.bar(r, mean3, yerr=CI3, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='Performing trust locally (fuzzy logic)')

#plt.bar(r+0.25, mean, yerr=sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
#        width = width, edgecolor = 'black',
#        label='Performing trust locally (weighted sum)')
plt.bar(r +0.25, mean2, yerr=CI2, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='Delegating trust')
plt.xticks(r + width/2,d)
plt.legend()
plt.ylim((0,80))
plt.show()

