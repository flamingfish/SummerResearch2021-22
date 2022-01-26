import geoplot as gplt
import geopandas as gpd
import geoplot.crs as gcrs
#import imageio
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import mapclassify as mc
import numpy as np

from shapely.geometry import Point

australia = gpd.read_file('australiaMap2/AUS_2021_AUST_GDA2020.shp')
# print(australia.head())
aus = australia[australia.AUS_CODE21=='AUS']
ax = gplt.polyplot(aus)
# plt.show()

maxTemp = gpd.read_file('data/AustralianAverageMaxTemp.csv')
is1975 = maxTemp['Year'] == '1975'
maxTemp1975 = maxTemp.loc[is1975]

maxTemp1975.long = maxTemp1975.long.astype(float)
maxTemp1975.lat = maxTemp1975.lat.astype(float)
maxTemp1975.Temp = maxTemp1975.Temp.astype(float)
geometry = [Point(xy) for xy in zip(maxTemp1975.long, maxTemp1975.lat)]
maxTemp1975 = maxTemp1975.drop(['long', 'lat'], axis=1)
maxTemp1975 = gpd.GeoDataFrame(maxTemp1975, crs="EPSG:4326", geometry=geometry)
print(maxTemp1975.head(15))
#print(maxTemp1975.index)
# maxTempNext = maxTemp1975.copy()

# def makeModify(year):
#     tempData = maxTemp.loc[maxTemp['Year'] == str(year)]
#     def modify(index):
#         locationName = tempData.iloc[index]['name']

#         maxTempNext.set_value('Temp', )

# maxTempNext.apply(lambda x: x)


#exit()

# print(maxTemp1975.head())
# gplt.pointplot(
#     maxTemp1975,
#     ax=ax,
#     hue='Temp',
#     legend=True,
#     k=None
# )

print('before voronoi')
gplt.voronoi(
    maxTemp1975,
    hue='Temp',
    clip=aus.simplify(0.001),
    cmap='viridis',
    legend=True,
    linewidth=0,
    edgecolor=None,
    k=None,
    ax=ax
)

# gplt.kdeplot(
#     maxTemp1975,
#     clip=aus.simplify(0.001),
#     shade=True,
#     ax=ax,
#     cmap='Reds'
# )

print('before point plot')
gplt.pointplot(
    maxTemp1975,
    color='black',
    ax=ax,
    s=1
)

print('done')

plt.show()
print('after show()')