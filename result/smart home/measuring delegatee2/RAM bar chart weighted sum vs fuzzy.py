import matplotlib.pyplot as plt
import statistics
import numpy as np
import scipy.stats as st
ram = []
ram_mean=[]
ram_sd=[]
Cinterval=[]
for p in range(1,11):
    ram.append([])
    ramAllfile=[]
    for z in range(1,11):
        for line in open(f'C:\\data generator\\e-health result 10 samples\\measuring delegatee2\\vary the number of delegatees\\result\\server_delegation{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                ramAllfile.append(int(lines[1])/1024) 
            except Exception:
                print('Line data error')
                #continue
    print(ramAllfile)
    conf = st.t.interval(0.95, len(ramAllfile)-1, loc=np.mean(ramAllfile), scale=st.sem(ramAllfile)) 
    conf = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf))
    Cinterval.append(conf)
    ram_mean.append(float("{:.5f}".format(statistics.mean(ramAllfile))))
    ram_sd.append(float("{:.5f}".format(statistics.stdev(ramAllfile))))
print("Mean = %s \nSD = %s \nCinterval = %s"%(ram_mean,ram_sd,";".join(str(x) for x in Cinterval)))

ram2 = []
ram2_mean=[]
ram2_sd=[]
C2interval=[]
for p in range(1,11):
    ram2.append([])
    ram2Allfile=[]
    for z in range(1,11):
        for line in open(f'C:\data generator\e-health result 10 samples\measuring delegatee2\\vary the number of delegators\\result\\server_delegation{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                ram2Allfile.append(int(lines[1])/1024) 
            except Exception:
                print('Line data error')
                #continue
    print(ram2Allfile)
    conf2 = st.t.interval(0.95, len(ram2Allfile)-1, loc=np.mean(ram2Allfile), scale=st.sem(ram2Allfile)) 
    conf2 = tuple(map(lambda x: isinstance(x, float) and round(x, 2) or x, conf2))
    C2interval.append(conf2)
    ram2_mean.append(float("{:.5f}".format(statistics.mean(ram2Allfile))))
    ram2_sd.append(float("{:.5f}".format(statistics.stdev(ram2Allfile))))
print("Mean = %s \nSD = %s \nCinterval = %s "%(ram2_mean,ram2_sd,";".join(str(x) for x in C2interval)))

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of RAM used by a delegate')
ax.set_xlabel('Number of trustees/trustors')
ax.set_ylabel('RAM usage (MB)')

plt.bar(r, ram_mean, yerr=ram_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='varying the number of trustees')
plt.bar(r + width, ram2_mean, yerr=ram2_sd, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='varying the number of trustors')
plt.xticks(r + width/2,d)
plt.legend()
plt.ylim((40,80))
plt.show()

