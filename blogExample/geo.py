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

usa = gpd.read_file('maps/cb_2018_us_state_20m.shp')
print(usa.head())

state_pop = pd.read_csv('data/nst-est2018-alldata.csv')
print(state_pop.head())

pop_states = usa.merge(state_pop, left_on='NAME', right_on='NAME')
print(pop_states.head())

# pop_states[pop_states.NAME=='California'].plot()
# plt.show()

path = gplt.datasets.get_path('contiguous_usa')
contiguous_usa = gpd.read_file(path)
# gplt.polyplot(contiguous_usa)
# plt.show()

path = gplt.datasets.get_path('usa_cities')
usa_cities = gpd.read_file(path)
print('########## USA cities: ###########')
print(usa_cities.head())
continental_usa_cities = usa_cities.query('STATE not in ["HI", "AK", "PR"]')
# gplt.pointplot(continental_usa_cities)
# plt.show()

# You can remove the projection attribute here:
# ax = gplt.polyplot(contiguous_usa, projection=gcrs.AlbersEqualArea())
# gplt.pointplot(continental_usa_cities, ax=ax)
# plt.show()
# ax = gplt.pointplot(continental_usa_cities)
# gplt.polyplot(contiguous_usa, ax=ax)
# plt.show()

# ax = gplt.polyplot(contiguous_usa, projection=gcrs.AlbersEqualArea())
# gplt.pointplot(
#     continental_usa_cities,
#     ax=ax,
#     hue="ELEV_IN_FT",
#     legend=True,
#     cmap='viridis',
#     k=None # This line turns the legend from categorical to continuous
# )
# plt.show()

# ax = gplt.polyplot(
#     contiguous_usa,
#     edgecolor='white',
#     facecolor='lightgray',
#     figsize=(12,8),
#     projection=gcrs.AlbersEqualArea()
# )
# gplt.pointplot(
#     continental_usa_cities,
#     ax=ax,
#     hue='ELEV_IN_FT',
#     cmap='Blues',
#     scheme='quantiles',
#     scale='ELEV_IN_FT',
#     limits=(1,10),
#     legend=True,
#     legend_var='scale',
#     legend_kwargs={'frameon': False},
#     legend_values=[-110, 1750, 3600, 5500, 7400],
#     legend_labels=['-110 feet', '1750 feet', '3600 feet', '5500 feet', '7400 feet']
# )
# ax.set_title('Cities in the continental US, by elevation', fontsize=16)
# plt.show()

# ax = gplt.polyplot(contiguous_usa, projection=gcrs.AlbersEqualArea())
# gplt.choropleth(
#     contiguous_usa,
#     hue="population",
#     edgecolor='white',
#     linewidth=1,
#     cmap='Greens',
#     legend=True,
#     scheme='FisherJenks',
#     # legend_labels=[
#     #     '<3 million', '3-6.7 million', '6.7-12.8 million',
#     #     '12.8-25 million', '25-37 million'
#     # ],
#     projection=gcrs.AlbersEqualArea(),
#     ax=ax
# )
# plt.show()

# boroughs = gpd.read_file(gplt.datasets.get_path('nyc_boroughs'))
# collisions = gpd.read_file(gplt.datasets.get_path('nyc_collision_factors'))
# ax = gplt.polyplot(boroughs, projection=gcrs.AlbersEqualArea())
# # gplt.kdeplot(collisions, cmap='Reds', shade=True, clip=boroughs, ax=ax)
# # This is me:
# gplt.pointplot(collisions, ax=ax)
# plt.show()

# ax = gplt.polyplot(contiguous_usa, projection=gcrs.AlbersEqualArea())
# gplt.kdeplot(
#     continental_usa_cities,
#     cmap='Reds',
#     shade=True,
#     clip=contiguous_usa,
#     ax=ax
# )
# plt.show()

# Skipping next example, which is about cartograms.

# scheme = mc.Quantiles(continental_usa_cities['ELEV_IN_FT'], k=10)
# gplt.pointplot(
#     continental_usa_cities,
#     projection=gcrs.AlbersEqualArea(),
#     hue='ELEV_IN_FT',
#     scheme=scheme,
#     cmap='inferno_r',
#     legend=True
# )
# plt.show()
# ^ The scheme triggered an internal error, couldn't be bothered to figure out why

# import warnings
# warnings.filterwarnings("ignore", "GeoSeries.isna", UserWarning)

# melbourne = gpd.read_file(gplt.datasets.get_path("melbourne"))
# df = gpd.read_file(gplt.datasets.get_path("melbourne_schools"))
# melbourne_primary_schools = df.query('School_Type == "Primary"')
# ax = gplt.voronoi(
#   melbourne_primary_schools,
#   clip=melbourne,
#   linewidth=0.5,
#   edgecolor="white",
#   projection=gcrs.Mercator()
# )
# gplt.polyplot(
#   melbourne,
#   edgecolor="None",
#   facecolor="lightgray",
#   ax=ax
# )
# gplt.pointplot(
#   melbourne_primary_schools,
#   color="black",
#   ax=ax,
#   s=1,
#   extent=melbourne.total_bounds
# )
# plt.title("Primary Schools in Greater Melbourne, 2018")
# plt.show()

# proj = gplt.crs.AlbersEqualArea(
#   central_longitude=-98,
#   central_latitude=39.5
# )
# ax = gplt.voronoi(
#   continental_usa_cities,
#   hue="ELEV_IN_FT",
#   clip=contiguous_usa,
#   projection=proj,
#   cmap="Reds",
#   legend=True,
#   edgecolor="white",
#   linewidth=0.01,
#   k=None
# )
# gplt.polyplot(
#   contiguous_usa,
#   ax=ax,
#   extent=contiguous_usa.total_bounds,
#   edgecolor="black",
#   linewidth=1,
#   zorder=1
# )
# plt.show()

#aus_maxT = pd.read_csv('data/AustralianAverageMaxTemp.csv')
#is1975 = aus_maxT['Year'] == '1975'

# australia = gpd.read_file('australiaMap/STE_2021_AUST_GDA2020.shp')
# print(australia.head())
# ax = gplt.polyplot(australia[australia.STE_NAME21=='Queensland'])
# gplt.polyplot(australia[australia.STE_NAME21=='New South Wales'], ax=ax)
# plt.xlim([110, 157])
# plt.ylim([-45, -10])
# plt.show()

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
maxTemp1975 = maxTemp1975.drop(['long', 'lat'], axis=1)
maxTemp1975 = gpd.GeoDataFrame(maxTemp1975, crs="EPSG:4326", geometry=geometry)
print(maxTemp1975.head())
gplt.pointplot(
    maxTemp1975,
    ax=ax,
    hue='Temp',
    legend=True,
    k=None
)

plt.pause(0.05)

# def update(frame):
#     maxTempFrame = maxTemp.loc[maxTemp['Year'] == str(1975+frame)]
#     maxTempFrame.long = maxTempFrame.long.astype(float)
#     maxTempFrame.lat = maxTempFrame.lat.astype(float)
#     maxTempFrame.Temp = maxTempFrame.Temp.astype(float)
#     geometry


# for year in range(1975, 2020):
#     maxTempFrame = maxTemp.loc[maxTemp['Year'] == str(year)]
#     maxTempFrame.long = maxTempFrame.long.astype(float)
#     maxTempFrame.lat = maxTempFrame.lat.astype(float)
#     maxTempFrame.Temp = maxTempFrame.Temp.astype(float)
#     geometry = [Point(xy) for xy in zip(maxTempFrame.long, maxTempFrame.lat)]
#     maxTempFrame = maxTempFrame.drop(['long', 'lat'], axis=1)
#     maxTempFrame = gpd.GeoDataFrame(maxTempFrame, crs="EPSG:4326", geometry=geometry)
#     gplt.pointplot(
#         maxTempFrame,
#         ax=ax,
#         hue='Temp',
#         legend=True,
#         k=None
#     )
#     plt.pause(0.05)

plt.show()

# ax = gplt.pointplot(maxTemp1975)
# gplt.polyplot(australia, ax=ax)
# plt.show()