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
import matplotlib.animation as animation

from os.path import dirname, join
current_dir = dirname(__file__)
australia = gpd.read_file(join(current_dir, 'australiaMap2/AUS_2021_AUST_GDA2020.shp'))
aus = australia[australia.AUS_CODE21=='AUS']
# print(aus.head())
# print(type(aus['geometry'][0]))
# exit()
# patch = PolygonPatch(aus['geometry'][0], transform=ax.transData)
# ax = gplt.polyplot(aus)

maxTemp = pd.read_csv(
    join(current_dir, 'data/AustralianAverageMaxTemp.csv'),
    dtype={
        'lat': np.float32,
        'long': np.float32,
        'elev': np.float16,
        'name': str,
        'Year': np.int16,
        'Temp': np.float32
    }
)

tempArray = maxTemp[['Year', 'lat', 'long', 'Temp']].to_numpy()
# print(tempArray)
# exit()

year = tempArray[:, 0]
lat = tempArray[:, 1]
long = tempArray[:, 2]
temp = tempArray[:, 3]
# pts = 1_000_000
# pts = 62_500
pts = 10_000

[x, y] = np.meshgrid(np.linspace(np.min(long), np.max(long), int(np.sqrt(pts))),
                     np.linspace(np.min(lat), np.max(lat), int(np.sqrt(pts))))
#x = np.matrix.flatten(x)
#y = np.matrix.flatten(y)

year = 1975
data = tempArray[tempArray[:, 0] == year]
lat = data[:, 1]
long = data[:, 2]
temp = data[:, 3]
z = Rbf(long, lat, temp, function='cubic')(x, y)

fig, ax = plt.subplots()
ax = gplt.polyplot(aus, ax=ax)
patch = PolygonPatch(aus['geometry'][0], transform=ax.transData)
implt = plt.imshow(z, extent=[np.min(x), np.max(x), np.min(y), np.max(y)], origin='lower',
        cmap='gist_rainbow')
implt.set_clip_path(patch)

scatterplt = plt.scatter(long, lat, s=10, c='#000000', zorder=20)

plt.colorbar(label='Elevation above sea level (m)')
plt.xlabel('Longitude (°)')
plt.ylabel('Latitude (°)')


def animate(i):
    global year, z
    year += 1
    data = tempArray[tempArray[:, 0] == year]
    lat = data[:, 1]
    long = data[:, 2]
    temp = data[:, 3]
    z = Rbf(long, lat, temp, function='cubic')(x, y)
    implt.set_data(z)
    # print('stepping')

    return implt, scatterplt

print('before animation')
ani = animation.FuncAnimation(fig, animate, interval=50, blit=True)
print('should be animating')
plt.show()

exit()
    

#z = griddata((long, lat), temp, (x, y), method='cubic')
z = Rbf(long, lat, temp, function='cubic')(x, y)
# x = np.matrix.flatten(x)
# y = np.matrix.flatten(y)
#z = np.matrix.flatten(z)


fig, ax = plt.subplots()
ax = gplt.polyplot(aus, ax=ax)
patch = PolygonPatch(aus['geometry'][0], transform=ax.transData)

# scatterplt = plt.scatter(x, y, 1, z, cmap='gist_rainbow')
# scatterplt.set_clip_path(patch)
implt = plt.imshow(z, extent=[np.min(x), np.max(x), np.min(y), np.max(y)], origin='lower',
        cmap='gist_rainbow')
implt.set_clip_path(patch)

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