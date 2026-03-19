import matplotlib.pyplot as plt
import numpy as np
import math

pdelegation=[2245.3065,2257.5932,2250.4930]
plocally=[2332.4764,2272.2170,2274.9350]
pWdelegation = np.divide(pdelegation,1000)
pWlocally = np.divide(plocally,1000)

pWdelegation_mean = np.mean(pWdelegation)
pWlocally_mean = np.mean(pWlocally)

pWdelegation_std = np.std(pWdelegation)
pWlocally_std = np.std(pWlocally)

y_value=[0,pWlocally_mean,pWdelegation_mean,0]
error=[0,pWlocally_std,pWdelegation_std,0]
print("%f %f"%(pWlocally_mean,pWdelegation_mean))
x= ['','Performing trust locally', 'Delegating trust','']
x_pos = np.arange(4) 

fig, ax = plt.subplots()
fig.set_size_inches(12, 8)
ax.bar(x_pos, y_value, yerr=error, align='center', alpha=0.8, color=['green','orange'], capsize=10, width=0.3)
ax.set_ylabel('Energy usage (Wh)')
ax.set_xticks(x_pos)
ax.set_xticklabels(x)
ax.set_title('Total Energy usage')
ax.yaxis.grid(True)

plt.tight_layout()
plt.show()