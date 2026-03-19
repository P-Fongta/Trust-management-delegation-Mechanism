import pandas as pd
import numpy as np
import itertools
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(15,10))
sns.set_context("notebook", font_scale=0.6, rc={"lines.linewidth": 0.5, 'font.family':'Helvetica'})

plt.subplot(2,2,1) # first heatmap
df = pd.read_excel("C:\\Users\\phong\\Documents\\python code\\book6.xlsx", sheet_name='Sheet1',nrows=15)
ax=sns.heatmap(df.set_index('Fruits').T, cmap="Blues",  cbar=1, square=True )
sns.despine()

plt.subplot(2,2,2) # first heatmap
df = pd.read_excel("C:\\Users\\phong\\Documents\\python code\\book6.xlsx", sheet_name='Sheet2',nrows=15)
ax=sns.heatmap(df.set_index('Vegetables').T, cmap="Blues",  cbar=1, square=True )
sns.despine()



plt.show()


