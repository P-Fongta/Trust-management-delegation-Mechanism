import matplotlib.pyplot as plt
import statistics
import numpy as np
import scipy.stats as st
import seaborn as sns
cpu_mean=[]
cpu_sd=[]
Cinterval=[]
conf_int = []
for p in range(1,11):
    cpu = []
    
    for line in open(f'C:\data generator\\smart_traffic\\fognode_towards_fog_end\\result\\Do_locally{p}.txt', "r"):
        try:
            lines = [i for i in line.split()]
            cpu_p1 = lines[0].split(":")[0]
            cpu_p23 = lines[0].split(":")[1].split(".")
            cpu_p2 = cpu_p23[0]
            cpu_p3 = cpu_p23[1]
            second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100)  
            #second = float("{:.3f}".format(second))
            cpu.append(second)
        except Exception:
            print('Line data error')
            #continue
    print(cpu)
    conf = st.t.interval(0.95, df=len(cpu)-1, loc=np.mean(cpu), scale=st.sem(cpu)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    Cinterval.append(conf)
    conf_int = 1.96 * statistics.stdev(cpu) / np.sqrt(len(cpu))
    cpu_mean.append(float("{:.3f}".format(statistics.mean(cpu))))
    cpu_sd.append(float("{:.3f}".format(statistics.stdev(cpu))))
print("Mean = %s \nSD = %s \nCinterval = %s"%(cpu_mean,cpu_sd,";".join(str(x) for x in Cinterval)))


cpu2_mean=[]
cpu2_sd=[]
C2interval=[]
for p in range(1,11):
    cpu2 = []
    
    for line in open(f'C:\data generator\\smart_traffic\\fognode_towards_fog_end_fuzzy\\result\\Do_locally{p}.txt', "r"):
        try:
            lines = [i for i in line.split()]
            cpu_p1 = lines[0].split(":")[0]
            cpu_p23 = lines[0].split(":")[1].split(".")
            cpu_p2 = cpu_p23[0]
            cpu_p3 = cpu_p23[1]
            second = (float(cpu_p1)*60) + (float(cpu_p2))+ (float(cpu_p3)/100)  
            #second = float("{:.3f}".format(second))
            cpu2.append(second)
        except Exception:
            print('Line data error')
            #continue
    print(cpu2)
    conf = st.t.interval(0.95, df=len(cpu2)-1, loc=np.mean(cpu2), scale=st.sem(cpu2)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    C2interval.append(conf)
    cpu2_mean.append(float("{:.3f}".format(statistics.mean(cpu2))))
    cpu2_sd.append(float("{:.3f}".format(statistics.stdev(cpu2))))

print("Mean = %s \nSD = %s \nCinterval = %s"%(cpu2_mean,cpu2_sd,";".join(str(x) for x in C2interval)))


d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('CPU Time of a fog node to perform trust management')
ax.set_xlabel('Number of target end nodes and fog nodes (Trustees)')
ax.set_ylabel('CPU Time (Seconds)')

plt.bar(r , cpu2_mean, yerr=cpu2_sd, color = 'tab:orange',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='fuzzy logic')
plt.bar(r+0.25, cpu_mean, yerr=cpu_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='weighted sum')

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

#plt.ylim((0,5.5))
#plt.xlim((0,16))
plt.show()

