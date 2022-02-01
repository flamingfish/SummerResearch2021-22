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

shapefile = gpd.read_file('GCCSA_2021_AUST_SHP_GDA2020/GCCSA_2021_AUST_GDA2020.shp')
greaterBrisbane = shapefile[shapefile['GCC_NAME21'] == 'Greater Brisbane']

#print(greaterBrisbane.loc[8, 'geometry'].bounds)
brisBounds = greaterBrisbane.loc[8, 'geometry'].bounds
#exit()

# Queensland coordinates
# maxLat = -9.942333
# minLat = -29.184142
# maxLong = 153.569427
# minLong = 137.945578

# Greater brisbane coordinates
maxLat = brisBounds[3] #-26.35
minLat = brisBounds[1] #-28.4
maxLong = brisBounds[2] #153.55
minLong = brisBounds[0] #152.5

freqData = pd.read_csv('DataDuplicatesRemoved.csv', dtype={
    'Name': str,
    'Long': np.float32,
    'Lat': np.float32,
    'Freq': np.float32
})

# Only want to look at data in greater brisbane
# freqData = freqData.loc[(freqData['Lat'] > minLat) & (freqData['Lat'] < maxLat) \
#         & (freqData['Long'] > minLong) & (freqData['Long'] < maxLong), :]

dataArray = freqData[['Lat', 'Long', 'Freq']].to_numpy()

australia = gpd.read_file('australiaMap/STE_2021_AUST_GDA2020.shp')
qld = australia[australia.STE_NAME21=='Queensland']
# print(qld.head())
# print(type(qld['geometry'][2])) # 2 is the index of Queensland in the dataframe
# exit()
# print(australia.head())
# ax = gplt.polyplot(qld)

# data = gpd.read_file('Data.csv')
# data = gpd.read_file('DataDuplicatesRemoved.csv')
# data.Long = data.Long.astype(float)
# data.Lat = data.Lat.astype(float)
# data.Freq = data.Freq.astype(float)

# dataArray = data[['Lat', 'Long', 'Freq']].to_numpy()

lat = dataArray[:, 0]
long = dataArray[:, 1]
freq = dataArray[:, 2]
pts = 10_000


[x, y] = np.meshgrid(np.linspace(minLong, maxLong, int(np.sqrt(pts))),
                     np.linspace(minLat, maxLat, int(np.sqrt(pts))))

z = griddata((long, lat), freq, (x, y), method='cubic', fill_value=50)
# z = Rbf(long, lat, freq, function='cubic')(x, y)

fig, ax = plt.subplots()
ax = gplt.polyplot(greaterBrisbane, ax=ax, zorder=40)
#patch = PolygonPatch(greaterBrisbane['geometry'][8], transform=ax.transData)
patch = PolygonPatch(qld['geometry'][2], transform=ax.transData)

# comment these 3 lines and then uncomment below for voronoi plot
#implt = plt.imshow(z, extent=[np.min(x), np.max(x), np.min(y), np.max(y)], origin='lower',
#        cmap='gist_rainbow')
#implt.set_clip_path(patch)

scatterplt = plt.scatter(long, lat, freq, freq, cmap='gist_rainbow')

geometry = [Point(xy) for xy in zip(freqData.Long, freqData.Lat)]
# data = data.drop(['Long', 'Lat'], axis=1)
data = gpd.GeoDataFrame(freqData, crs="EPSG:4326", geometry=geometry)

# uncomment this for voronoi plot
# gplt.voronoi(
#     data,
#     hue='Freq',
#     clip=qld.simplify(0.001),
#     cmap='gist_rainbow',
#     legend=True,
#     linewidth=0,
#     edgecolor=None,
#     k=None,
#     ax=ax
# )

plt.colorbar(label='Frequency (Hz)')
plt.xlabel('Longitude (°)')
plt.ylabel('Latitude (°)')

# gplt.pointplot(
#     maxTemp1975,
#     color='black',
#     ax=ax,
#     s=1
# )
#plt.scatter(long, lat, s=10, c='#000000', zorder=20)
plt.show()