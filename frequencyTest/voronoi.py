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
ax = gplt.polyplot(qld)
# print(qld.head())
# print(type(qld['geometry'][2])) # 2 is the index of Queensland in the dataframe
# exit()
# print(australia.head())
# ax = gplt.polyplot(qld)

data = gpd.read_file('Data.csv')
data.Long = data.Long.astype(float)
data.Lat = data.Lat.astype(float)
data.Freq = data.Freq.astype(float)
geometry = [Point(xy) for xy in zip(data.Long, data.Lat)]
data = data.drop(['Long', 'Lat'], axis=1)
data = gpd.GeoDataFrame(data, crs="EPSG:4326", geometry=geometry)

gplt.voronoi(
    data,
    hue='Freq',
    clip=qld.simplify(0.001),
    cmap='gist_rainbow',
    legend=True,
    linewidth=0,
    edgecolor=None,
    k=None,
    ax=ax
)

gplt.pointplot(
    data,
    color='black',
    ax=ax,
    s=3
)

# Queensland coordinates
maxLat = -9.942333
minLat = -29.184142
maxLong = 153.569427
minLong = 137.945578

plt.xlim([minLong, maxLong])
plt.ylim([minLat, maxLat])
plt.show()