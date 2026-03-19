import matplotlib.pyplot as plt
import statistics
import numpy as np
V1, V2, V3 = [],[],[]
C1,C2 ,C3 = [],[],[]
W1,W2 ,W3 = [],[],[]
dV1, dV2, dV3 = [],[],[]
dC1,dC2 ,dC3 = [],[],[]
dW1,dW2 ,dW3 = [],[],[]
d = [i for i in range(1,9001)]

for line in open('C:\data generator\graph\\new_graph\locally_adj\power1.txt', 'r'):
    lines = [i for i in line.split()]
    V1.append(float(lines[0]))
    C1.append(float(lines[1]))
    W1.append(float(lines[2]))

for line in open('C:\data generator\graph\\new_graph\locally_adj\power2.txt', 'r'):
    lines = [i for i in line.split()]
    V2.append(float(lines[0]))
    C2.append(float(lines[1]))
    W2.append(float(lines[2]))
for line in open('C:\data generator\graph\\new_graph\locally_adj\power3.txt', 'r'):
    lines = [i for i in line.split()]
    V3.append(float(lines[0]))
    C3.append(float(lines[1]))
    W3.append(float(lines[2]))
    #print("%s"%(V3))
W_mean = [float("{:.5f}".format(statistics.mean(k)/1000)) for k in zip(W1, W2,W3)]
W_sd = [float("{:.5f}".format(statistics.stdev(k)/1000)) for k in zip(W1, W2,W3)]

for line in open('C:\data generator\graph\\new_graph\delegation_adj\power1.txt', 'r'):
    lines = [i for i in line.split()]
    dV1.append(float(lines[0]))
    dC1.append(float(lines[1]))
    dW1.append(float(lines[2]))
for line in open('C:\data generator\graph\\new_graph\delegation_adj\power2.txt', 'r'):
    lines = [i for i in line.split()]
    dV2.append(float(lines[0]))
    dC2.append(float(lines[1]))
    dW2.append(float(lines[2]))
for line in open('C:\data generator\graph\\new_graph\delegation_adj\power3.txt', 'r'):
    lines = [i for i in line.split()]
    dV3.append(float(lines[0]))
    dC3.append(float(lines[1]))
    dW3.append(float(lines[2]))
dW_mean = [float("{:.5f}".format(statistics.mean(k)/1000)) for k in zip(dW1, dW2,dW3)]
dW_sd = [float("{:.5f}".format(statistics.stdev(k)/1000)) for k in zip(dW1, dW2,dW3)]


fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)

tick = np.arange(0,9001,600)
x_ticks_labels = ['0m','10m','20m','30m','40m','50m','1h','1:10h','1:20h','1:30h','1:40h','1:50h','2h','2:10h','2:20h','2:30h']

ax.set_title('Power Consumption')
ax.set_xlabel('Time')
ax.set_ylabel('Power Consumption (Watt)')

ax.plot(d, W_mean, '-', color='tab:orange',label="Performing trust locally",linewidth=0.5)
# create a confidence band
y_lower = [float(i) + float(k)  for (i,k) in zip(W_mean,W_sd)]
y_upper = [float(i) - float(k)  for (i,k) in zip(W_mean,W_sd)]
ax.fill_between(d, y_lower, y_upper, alpha=0.05, color='tab:orange')

d2 = [i for i in range(1,10805)]

ax.plot(d, dW_mean, '-', color='tab:green',label="Delegating trust",linewidth=0.5)
# create a confidence band

dy_lower = [float(i) + float(k)  for (i,k) in zip(dW_mean,dW_sd)]
dy_upper = [float(i) - float(k)  for (i,k) in zip(dW_mean,dW_sd)]
ax.fill_between(d, dy_lower, dy_upper, alpha=0.05, color='tab:green')

plt.legend(loc='upper right')
plt.ylim((0,3))
#ax.yaxis.grid(True)

ax.set_xticks(tick)
ax.set_xticklabels(x_ticks_labels)
#plt.tight_layout()
#plt.ylim((600,900))
plt.xlim((0,9001))
plt.show()
