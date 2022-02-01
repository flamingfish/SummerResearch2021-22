import geopandas as gpd
import geoplot as gplt
from shapely.geometry import Point
import matplotlib.pyplot as plt
import numpy as np


australia = gpd.read_file('australiaMap2/AUS_2021_AUST_GDA2020.shp')
print(australia.head())
ax = gplt.polyplot(australia[australia.AUS_CODE21=='AUS'])
# # plt.show()

maxTemp = gpd.read_file('data/AustralianAverageMaxTemp.csv')
is1975 = maxTemp['Year'] == '1975'
maxTemp1975 = maxTemp.loc[is1975]

maxTemp1975.long = maxTemp1975.long.astype(float)
maxTemp1975.lat = maxTemp1975.lat.astype(float)
maxTemp1975.Temp = maxTemp1975.Temp.astype(float)
geometry = [Point(xy) for xy in zip(maxTemp1975.long, maxTemp1975.lat)]
#maxTemp1975 = maxTemp1975.drop(['long', 'lat'], axis=1)
maxTemp1975 = gpd.GeoDataFrame(maxTemp1975, crs="EPSG:4326", geometry=geometry)
print(maxTemp1975.head())
# gplt.pointplot(
#     maxTemp1975,
#     ax=ax,
#     hue='Temp',
#     legend=True,
#     k=None
# )

MAX_SIZE = 200
MIN_SIZE = 20
SIZE_RANGE = MAX_SIZE - MIN_SIZE

temp = maxTemp1975['Temp']
tempRange = np.max(temp) - np.min(temp)
sizes = (temp - np.min(temp)) / tempRange * SIZE_RANGE + MIN_SIZE

#sizes = maxTemp1975['Temp'] / np.max(maxTemp1975['Temp']) * 200 # scaling factor for dot sizes

scatterplt = ax.scatter(maxTemp1975['long'], maxTemp1975['lat'], c=temp, s=sizes, alpha=0.3)

plt.show()