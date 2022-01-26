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

australia = gpd.read_file('australiaMap2/AUS_2021_AUST_GDA2020.shp')
aus = australia[australia.AUS_CODE21=='AUS']
# print(aus.head())
# print(type(aus['geometry'][0]))
# exit()
# patch = PolygonPatch(aus['geometry'][0], transform=ax.transData)
# ax = gplt.polyplot(aus)

maxTemp = gpd.read_file('data/AustralianAverageMaxTemp.csv')
is1975 = maxTemp['Year'] == '1975'
maxTemp1975 = maxTemp.loc[is1975]
maxTemp1975.long = maxTemp1975.long.astype(float)
maxTemp1975.lat = maxTemp1975.lat.astype(float)
maxTemp1975.Temp = maxTemp1975.Temp.astype(float)

tempArray = maxTemp1975[['lat', 'long', 'Temp']].to_numpy()
# print(tempArray)
# exit()

lat = tempArray[:, 0]
long = tempArray[:, 1]
temp = tempArray[:, 2]
pts = 1_000_000

[x, y] = np.meshgrid(np.linspace(np.min(long), np.max(long), int(np.sqrt(pts))),
                     np.linspace(np.min(lat), np.max(lat), int(np.sqrt(pts))))
x = np.matrix.flatten(x)
y = np.matrix.flatten(y)

#z = griddata((long, lat), temp, (x, y), method='cubic')
z = Rbf(long, lat, temp, function='cubic')(x, y)
# x = np.matrix.flatten(x)
# y = np.matrix.flatten(y)
z = np.matrix.flatten(z)

fig, ax = plt.subplots()
ax = gplt.polyplot(aus, ax=ax)
patch = PolygonPatch(aus['geometry'][0], transform=ax.transData)

scatterplt = plt.scatter(x, y, 1, z, cmap='gist_rainbow')
scatterplt.set_clip_path(patch)
plt.colorbar(label='Elevation above sea level (m)')
plt.xlabel('Longitude (°)')
plt.ylabel('Latitude (°)')

# gplt.pointplot(
#     maxTemp1975,
#     color='black',
#     ax=ax,
#     s=1
# )
plt.scatter(long, lat)
plt.show()