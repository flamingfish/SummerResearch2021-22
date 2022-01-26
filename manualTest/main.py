import geoplot as gplt
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

australia = gpd.read_file('australiaMap2/AUS_2021_AUST_GDA2020.shp')
aus = australia[australia.AUS_CODE21=='AUS']
ax = gplt.polyplot(aus)
maxTemp = gpd.read_file('data/AustralianAverageMaxTemp.csv')
is1975 = maxTemp['Year'] == '1975'
maxTemp1975 = maxTemp.loc[is1975]

maxTemp1975.long = maxTemp1975.long.astype(float)
maxTemp1975.lat = maxTemp1975.lat.astype(float)
maxTemp1975.Temp = maxTemp1975.Temp.astype(float)
geometry = [Point(xy) for xy in zip(maxTemp1975.long, maxTemp1975.lat)]
maxTemp1975 = maxTemp1975.drop(['long', 'lat'], axis=1)
maxTemp1975 = gpd.GeoDataFrame(maxTemp1975, crs="EPSG:4326", geometry=geometry)
