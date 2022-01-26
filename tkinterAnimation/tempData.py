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

# ============= Data stuff ===============

from os.path import dirname, join
current_dir = dirname(__file__)
australia = gpd.read_file(join(current_dir, 'australiaMap2/AUS_2021_AUST_GDA2020.shp'))
aus = australia[australia.AUS_CODE21=='AUS']

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

print('Completed extracting data')

# ================ Tkinter stuff ==================

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
ax = fig.add_subplot(111)
# line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
# ax.set_xlabel('time [s]')
# ax.set_ylabel('f(t)')

# My stuff:
ax = gplt.polyplot(aus, ax=ax)
patch = PolygonPatch(aus['geometry'][0], transform=ax.transData)
implt = ax.imshow(z, extent=[np.min(x), np.max(x), np.min(y), np.max(y)], origin='lower',
        cmap='gist_rainbow')
implt.set_clip_path(patch)

scatterplt = ax.scatter(long, lat, s=10, c='#000000', zorder=20)
fig.colorbar(implt, label='Temperature (°C)', ax=ax)
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

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
button_quit.pack(side=tkinter.BOTTOM)
#slider_update.pack(side=tkinter.BOTTOM)
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

tkinter.mainloop()