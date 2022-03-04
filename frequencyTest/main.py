import geoplot as gplt
import geopandas as gpd
import geoplot.crs as gcrs
#import imageio
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import mapclassify as mc
import numpy as np
from descartes import PolygonPatch

from scipy.interpolate import griddata
from scipy.interpolate import Rbf
from shapely.geometry import Point

# australia = gpd.read_file('australiaMap2/AUS_2021_AUST_GDA2020.shp')
# aus = australia[australia.AUS_CODE21=='AUS']
# print(aus.head())
# print(type(aus['geometry'][0])) # 0 is the index in the dataframe
# exit()
# patch = PolygonPatch(aus['geometry'][0], transform=ax.transData)
# ax = gplt.polyplot(aus)

australia = gpd.read_file('australiaMap/STE_2021_AUST_GDA2020.shp')
qld = australia[australia.STE_NAME21=='Queensland']
# print(qld.head())
# print(type(qld['geometry'][2])) # 2 is the index of Queensland in the dataframe
# exit()
# print(australia.head())
# ax = gplt.polyplot(qld)

# data = gpd.read_file('Data.csv')
data = gpd.read_file('DataDuplicatesRemoved.csv')
data.Long = data.Long.astype(float)
data.Lat = data.Lat.astype(float)
data.Freq = data.Freq.astype(float)

dataArray = data[['Lat', 'Long', 'Freq']].to_numpy()

lat = dataArray[:, 0]
long = dataArray[:, 1]
freq = dataArray[:, 2]
pts = 1_000_000

# Queensland coordinates
maxLat = -9.942333
minLat = -29.184142
maxLong = 153.569427
minLong = 137.945578

# Greater brisbane coordinates
# maxLat = -26.35
# minLat = -28.4
# maxLong = 153.55
# minLong = 152.5


[x, y] = np.meshgrid(np.linspace(minLong, maxLong, int(np.sqrt(pts))),
                     np.linspace(minLat, maxLat, int(np.sqrt(pts))))
x = np.matrix.flatten(x)
y = np.matrix.flatten(y)

# comment out one of these - they are two different functions for interpolation
z = griddata((long, lat), freq, (x, y), method='cubic', fill_value=50)
# z = Rbf(long, lat, freq, function='multiquadric')(x, y)


# x = np.matrix.flatten(x)
# y = np.matrix.flatten(y)
z = np.matrix.flatten(z)

fig, ax = plt.subplots()
ax = gplt.polyplot(qld, ax=ax)
patch = PolygonPatch(qld['geometry'][2], transform=ax.transData)

scatterplt = plt.scatter(x, y, 1, z, cmap='gist_rainbow')
scatterplt.set_clip_path(patch)
plt.colorbar(label='Frequency (Hz)')
plt.xlabel('Longitude (°)')
plt.ylabel('Latitude (°)')

# gplt.pointplot(
#     maxTemp1975,
#     color='black',
#     ax=ax,
#     s=1
# )
plt.scatter(long, lat, s=10, c='#000000', zorder=20)
plt.show()