import matplotlib.pyplot as plt
import statistics
import numpy as np
import scipy.stats as st
import math
cpu = []
cpu_mean=[]
cpu_sd=[]
Cinterval=[]
CIN=[]
for p in range(1,11):
    cpu.append([])
    cpuAllfile=[]
    for z in range(1,11):
        for line in open(f'C:\data generator\e-health result 10 samples\locally\\weighted sum\\result\\Do_locally{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                cpu_p1 = lines[0].split(":")[0]
                cpu_p23 = lines[0].split(":")[1].split(".")
                cpu_p2 = cpu_p23[0]
                cpu_p3 = cpu_p23[1]
                second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100)  
                #second = float("{:.3f}".format(second))
                cpuAllfile.append(second)
            except Exception:
                print('Line data error')
                #continue
    print(cpuAllfile)
    
    cpu_mean.append(float("{:.3f}".format(statistics.mean(cpuAllfile))))
    cpu_sd.append(float("{:.3f}".format(statistics.stdev(cpuAllfile))))

    #calculate CI
    conf = st.t.interval(0.95, df=len(cpuAllfile)-1, loc=np.mean(cpuAllfile), scale=st.sem(cpuAllfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    CIN.append(conf)
    CI = 2.262*(statistics.stdev(cpuAllfile)/math.sqrt(len(cpuAllfile)))
    Cinterval.append(CI)
    #print("%.2f %.2f"%(statistics.mean(cpuAllfile)-CI,statistics.mean(cpuAllfile)+CI))
print("Mean = %s \nSD = %s \nCinterval = %s"%(cpu_mean,cpu_sd,";".join(str(x) for x in CIN)))

cpu2 = []
cpu2_mean=[]
cpu2_sd=[]
C2interval=[]
CIN2=[]
for p in range(1,11):
    cpu2.append([])
    cpu2Allfile=[]
    for z in range(1,11):
        for line in open(f'C:\data generator\e-health result 10 samples\locally\\fuzzy\\result\\Do_locally{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                cpu_p1 = lines[0].split(":")[0]
                cpu_p23 = lines[0].split(":")[1].split(".")
                cpu_p2 = cpu_p23[0]
                cpu_p3 = cpu_p23[1]
                second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100)  
                #second = float("{:.3f}".format(second))
                cpu2Allfile.append(second)
            except Exception:
                print('Line data error')
                #continue
    print(cpu2Allfile)
    
    cpu2_mean.append(float("{:.3f}".format(statistics.mean(cpu2Allfile))))
    cpu2_sd.append(float("{:.3f}".format(statistics.stdev(cpu2Allfile))))

    #calculate CI
    conf = st.t.interval(0.95, df=len(cpu2Allfile)-1, loc=np.mean(cpu2Allfile), scale=st.sem(cpu2Allfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    CIN2.append(conf)
    CI = 2.262*(statistics.stdev(cpu2Allfile)/math.sqrt(len(cpu2Allfile)))
    C2interval.append(CI)
    #print("%.2f %.2f"%(statistics.mean(cpuAllfile)-CI,statistics.mean(cpuAllfile)+CI))
print("Mean = %s \nSD = %s \nCinterval = %s"%(cpu2_mean,cpu2_sd,";".join(str(x) for x in CIN2)))

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('CPU Time used by an end node')
ax.set_xlabel('Number of fog nodes')
ax.set_ylabel('CPU Time (Seconds)')

plt.bar(r, cpu_mean, yerr=Cinterval, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='Weighted sum')
plt.bar(r + width, cpu2_mean, yerr=C2interval, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='Fuzzy logic')
plt.xticks(r + width/2,d)
plt.legend()
#ax.bar(d, cpu_mean, yerr=cpu_sd, align='center', alpha=0.8, color=['green'], capsize=10, width=0.5)
#ax.plot(d, cpu_mean, '-', color='tab:orange',label="Performing trust locally",linewidth=0.5)
# create a confidence band
#y_lower = [float(i) + float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#y_upper = [float(i) - float(k)  for (i,k) in zip(cpu_mean,cpu_sd)]
#ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')

#ax.set_xticks(d)
#ax.set_xticklabels(d)

#plt.legend(loc='upper right')

#plt.ylim((0,1000))
#plt.xlim((0,16))
plt.show()

