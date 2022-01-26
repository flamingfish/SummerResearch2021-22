import geopandas
import matplotlib.pyplot as plt

outline = geopandas.read_file('STE_2021_AUST_GDA2020.shp')
#print(outline.head())
outline.plot()
plt.show()
