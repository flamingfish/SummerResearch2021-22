import tkinter

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

import geoplot as gplt
import geopandas as gpd
import geoplot.crs as gcrs
#import imageio
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import mapclassify as mc
#import numpy as np
from descartes import PolygonPatch

from scipy.interpolate import griddata
from scipy.interpolate import Rbf
from shapely.geometry import Point
import matplotlib.animation as animation
from os.path import dirname, join

# My imports
from readFuncs import threaded_read_day, read_gps, read_hour
from zoom_factory import zoom_factory
from reset_detail import reset_detail_factory

# ============= Data stuff ===============

pmus = [
    'ECCATE',
    'Ecblue0203',
    'Ecmopa02',
    'Ecblue04',
    'Ecrowe',
    'X876428',
    'Ecgoot',
    'Echowa01',
    'X877522',
    'X10922-E',
    'X1064388-A',
    'X18755-E',
    'X412017',
    'X831-O',
    'X34249-F',
    'X414042',
    'X4460-K',
    'X742845',
#    'X756850',
    'X410035',
    'X2189666',
    'X18524-B',
#    'X94855-A',
    'X22116-D',
    'X2264432',
    'X2264597',
    'X841621',
    'X467127',
    'X71950-A',
    'X61106-C'
]

gps_data = read_gps('D:\\PMU\\PMU_GPS.xlsx')
hour_data = read_hour('D:\\PMU\\2021\\07\\28', pmus, '00', 0, 3)

hour_data.columns = hour_data.columns.str.lower()
gps_data.index = gps_data.index.str.lower()

# print(hour_data)
# print(gps_data)
# print(gps_data.loc[hour_data.columns.tolist(), :])

relevant_gps_data = gps_data.loc[hour_data.columns.tolist(), :]
timestamp = hour_data.index[0]
freq = hour_data.loc[timestamp, :]
freq.name = 'Frequency'
print(freq)

timeslice_data = pd.concat([relevant_gps_data, freq], axis=1)
print(timeslice_data)
timeslice_data_arr = timeslice_data.to_numpy()
print(timeslice_data_arr)
#exit()

#print(gps_data.loc['ecblue04', 'Latitude'])
#exit()

# lat = gps_data['Latitude']
# long = gps_data['Longitude']
# freq = hour_data.iloc[0, :]

# timestamp = hour_data.index[0]
# freq = hour_data.loc[timestamp, :]


# print(lat)
# print(long)
# print(freq)

# lat = lat

# timeslice = np.zeros(freq.size, 3)
# timeslice[:, 0] = long.to_numpy()
# timeslice[:, 1] = lat.to_numpy()


# exit()

# current_dir = dirname(__file__)
# australia = gpd.read_file(join(current_dir, 'australiaMap2/AUS_2021_AUST_GDA2020.shp'))
# aus = australia[australia.AUS_CODE21=='AUS']

# maxTemp = pd.read_csv(
#     join(current_dir, 'data/AustralianAverageMaxTemp.csv'),
#     dtype={
#         'lat': np.float32,
#         'long': np.float32,
#         'elev': np.float16,
#         'name': str,
#         'Year': np.int16,
#         'Temp': np.float32
#     }
# )

# tempArray = maxTemp[['Year', 'lat', 'long', 'Temp']].to_numpy()
# print(tempArray)
# exit()

# year = tempArray[:, 0]
# lat = tempArray[:, 1]
# long = tempArray[:, 2]
# temp = tempArray[:, 3]
# pts = 1_000_000
# pts = 62_500
long = timeslice_data_arr[:, 0]
lat = timeslice_data_arr[:, 1]
freq = timeslice_data_arr[:, 2]
pts = 10_000

# [x, y] = np.meshgrid(np.linspace(np.min(long), np.max(long), int(np.sqrt(pts))),
#                      np.linspace(np.min(lat), np.max(lat), int(np.sqrt(pts))))
# #x = np.matrix.flatten(x)
# #y = np.matrix.flatten(y)

# # year = 1975
# # data = tempArray[tempArray[:, 0] == year]
# # lat = data[:, 1]
# # long = data[:, 2]
# # temp = data[:, 3]
# z = Rbf(long, lat, freq, function='cubic')(x, y)
# print(z)

# Queensland coordinates
maxLat = -9.942333
minLat = -29.184142
maxLong = 153.569427
minLong = 137.945578

[x, y] = np.meshgrid(np.linspace(minLong, maxLong, int(np.sqrt(pts))),
                     np.linspace(minLat, maxLat, int(np.sqrt(pts))))

z = griddata((long, lat), freq, (x, y), method='cubic', fill_value=50)

print('Completed extracting data')


# ================ Map stuff ==================

australia = gpd.read_file('australiaMap/STE_2021_AUST_GDA2020.shp')
qld = australia[australia.STE_NAME21=='Queensland']
maxLat = -9.942333
minLat = -29.184142
maxLong = 153.569427
minLong = 137.945578

# ================ Tkinter stuff ==================

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
ax = fig.add_subplot(111)
# line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
# ax.set_xlabel('time [s]')
# ax.set_ylabel('f(t)')

print([np.min(x), np.max(x), np.min(y), np.max(y)])

# My stuff:
ax = gplt.polyplot(qld, ax=ax)
patch = PolygonPatch(qld['geometry'][2], transform=ax.transData)
implt = ax.imshow(z, extent=[np.min(x), np.max(x), np.min(y), np.max(y)], origin='lower',
        cmap='gist_rainbow')
# implt = ax.imshow(z, extent=[minLong, maxLong, minLat, maxLat], origin='lower',
#         cmap='gist_rainbow')
implt.set_clip_path(patch)

scatterplt = ax.scatter(long, lat, s=10, c='#000000', zorder=20)
fig.colorbar(implt, label='Frequency (Hz)', ax=ax)
plt.xlabel('Longitude (°)')
plt.ylabel('Latitude (°)')


canvas = FigureCanvasTkAgg(fig, master=root) # A tk.DrawingArea.
canvas.draw()

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
    'key_press_event',
    lambda event: print(f'you pressed {event.key}')
)
canvas.mpl_connect('key_press_event', key_press_handler)

button_quit = tkinter.Button(master=root, text='Quit', command=root.quit)

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
button_quit.pack(side=tkinter.BOTTOM)
#slider_update.pack(side=tkinter.BOTTOM)
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

coords = [x, y, z]
index = 0
def animate(i):
    global index, z
    index += 1
    freq = hour_data.iloc[index, :]
    freq.name = 'Frequency'
    timeslice_data = pd.concat([relevant_gps_data, freq], axis=1)
    timeslice_data_arr = timeslice_data.to_numpy()
    coords[2] = griddata((long, lat), freq, (coords[0], coords[1]), method='cubic', fill_value=50)
    implt.set_data(coords[2])

    # data = tempArray[tempArray[:, 0] == year]
    # lat = data[:, 1]
    # long = data[:, 2]
    # temp = data[:, 3]
    # z = Rbf(long, lat, temp, function='cubic')(x, y)
    # implt.set_data(z)
    # print('stepping')

    return implt, scatterplt

print('before animation')
ani = animation.FuncAnimation(fig, animate, interval=50, blit=True)
print('should be animating')

# add the ability to zoom:
reset_detail = reset_detail_factory(pts, long, lat, freq, implt)
ax.figure.canvas.toolbar.push_current()
zoom_func = zoom_factory(ax, base_scale=1.1, callback=reset_detail, coords=coords)

tkinter.mainloop()