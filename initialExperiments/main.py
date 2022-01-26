import matplotlib
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
#%matplotlib inline

nb = 'STE_2021_AUST_GDA2020.shp'
regions = gpd.read_file(nb)

regions.sample(5)

outline = gpd.read_file('STE_2021_AUST_GDA2020.shp')
outline.head()
ax = outline.plot()

plt.show()