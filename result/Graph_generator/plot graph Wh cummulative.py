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

W1_second = np.divide(W1,3600000)
W2_second = np.divide(W2,3600000)
W3_second = np.divide(W3,3600000)
cum_W1_second=np.cumsum(W1_second)
cum_W2_second=np.cumsum(W2_second)
cum_W3_second=np.cumsum(W3_second)

cum_W3_second_mean = [float("{:.5f}".format(statistics.mean(k))) for k in zip(cum_W1_second, cum_W2_second,cum_W3_second)]
cum_dW3_second_sd = [float("{:.5f}".format(statistics.stdev(k))) for k in zip(cum_W1_second, cum_W2_second,cum_W3_second)]

dW1_second = np.divide(dW1,3600000)
dW2_second = np.divide(dW2,3600000)
dW3_second = np.divide(dW3,3600000)
cum_dW1_second=np.cumsum(dW1_second)
cum_dW2_second=np.cumsum(dW2_second)
cum_dW3_second=np.cumsum(dW3_second)

cum_dW3_second_mean = [float("{:.5f}".format(statistics.mean(k))) for k in zip(cum_dW1_second, cum_dW2_second,cum_dW3_second)]
cum_dW3_second_sd = [float("{:.5f}".format(statistics.stdev(k))) for k in zip(cum_dW1_second, cum_dW2_second,cum_dW3_second)]

fig, ax = plt.subplots() 
fig.set_size_inches(12, 8)
ax.set_title('Total energy usage')
ax.set_xlabel('Time')
ax.set_ylabel('Energy usage (Wh)')


ax.plot(d, cum_W3_second_mean, '-', color='tab:orange',label="Performing trust locally",linewidth=1.5)
# create a confidence band
y_lower = [float(i) + float(k)  for (i,k) in zip(cum_W3_second_mean,cum_dW3_second_sd)]
y_upper = [float(i) - float(k)  for (i,k) in zip(cum_W3_second_mean,cum_dW3_second_sd)]
ax.fill_between(d, y_lower, y_upper, alpha=0.1, color='tab:orange')

ax.plot(d, cum_dW3_second_mean, '-', color='tab:green',label="Delegating trust",linewidth=1.5)
# create a confidence band

dy_lower = [float(i) + float(k)  for (i,k) in zip(cum_dW3_second_mean,cum_dW3_second_sd)]
dy_upper = [float(i) - float(k)  for (i,k) in zip(cum_dW3_second_mean,cum_dW3_second_sd)]
ax.fill_between(d, dy_lower, dy_upper, alpha=0.1, color='tab:green')

tick = np.arange(0,9001,600)
x_ticks_labels = ['0m','10m','20m','30m','40m','50m','1h','1:10h','1:20h','1:30h','1:40h','1:50h','2h','2:10h','2:20h','2:30h']

print(tick)
ax.margins(x=0, y=0)
plt.legend(loc='upper right')
plt.ylim((0,3))
ax.yaxis.grid(True)
plt.xlim((0,9000))
ax.set_xticks(tick)
ax.set_xticklabels(x_ticks_labels)
plt.tight_layout()
plt.show()
