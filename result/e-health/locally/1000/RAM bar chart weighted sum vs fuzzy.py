import matplotlib.pyplot as plt
import statistics
import numpy as np

ramfile01_max=[]
ramfile02_max=[]
ramfile03_max=[]
ram = []
for p in range(1,11):
    ram.append([])
    for z in range(1,4):
        #i=0
        ramEachfile=[]
        
        for line in open(f'C:\\data generator\\e-health\locally\\1000\\weightsum\\result\\Do_locally{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                ramEachfile.append(int(lines[1])) 
            except Exception:
                print('Line data error')
                #continue
        xv = max(ramEachfile)
        ram[p-1].append(xv)
    print(ram[p-1])

ram2 = []
for p in range(1,11):
    ram2.append([])
    for z in range(1,4):
        #i=0
        ram2Eachfile=[]
        
        for line in open(f'C:\\data generator\\e-health\locally\\1000\\fuzzy\\result\\Do_locally{p}-{z}.txt', "r"):
            try:
                lines = [i for i in line.split()]
                ram2Eachfile.append(int(lines[1])) 
            except Exception:
                print('Line data error')
                #continue
        xv = max(ram2Eachfile)
        ram2[p-1].append(xv)
    print(ram2[p-1])

ram_mean=[]
ram_sd=[]
for z in range(0,10):
    k=[]
    k.append(ram[z][0]/1024)
    k.append(ram[z][1]/1024)
    k.append(ram[z][2]/1024)
    ram_mean.append(float("{:.5f}".format(statistics.mean(k))))
    ram_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print("Ram Mean: %s"%ram_mean)
print("Ram SD: %s"%ram_sd)

ram2_mean=[]
ram2_sd=[]
for z in range(0,10):
    k=[]
    k.append(ram2[z][0]/1024)
    k.append(ram2[z][1]/1024)
    k.append(ram2[z][2]/1024)
    ram2_mean.append(float("{:.5f}".format(statistics.mean(k))))
    ram2_sd.append(float("{:.5f}".format(statistics.stdev(k))))
print("Ram2 Mean: %s"%ram2_mean)
print("Ram2 SD: %s"%ram2_sd)

d = [i for i in range(1,11)]
n=10
r = np.arange(n)
width = 0.25

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('The amount of RAM used by a medical sensor')
ax.set_xlabel('Number of fog nodes (Trustees)')
ax.set_ylabel('RAM usage (MB)')

plt.bar(r, ram_mean, yerr=ram_sd, color = 'tab:blue',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
        label='Weighted sum')
plt.bar(r + width, ram2_mean, yerr=ram2_sd, color = 'tab:green',align='center', alpha=0.8,capsize=8,
        width = width, edgecolor = 'black',
       label='Fuzzy logic')
plt.xticks(r + width/2,d)
plt.legend()
plt.ylim((0,100))
plt.show()

