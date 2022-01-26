import tkinter

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

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

# my imports:
from zoom_factory import zoom_factory

# shapefile = gpd.read_file('GCCSA_2021_AUST_SHP_GDA2020/GCCSA_2021_AUST_GDA2020.shp')
# greaterBrisbane = shapefile[shapefile['GCC_NAME21'] == 'Greater Brisbane']
australia = gpd.read_file('australiaMap/STE_2021_AUST_GDA2020.shp')
qld = australia[australia.STE_NAME21=='Queensland']

#print(greaterBrisbane.loc[8, 'geometry'].bounds)
#brisBounds = greaterBrisbane.loc[8, 'geometry'].bounds
#exit()

# Queensland coordinates
maxLat = -9.942333
minLat = -29.184142
maxLong = 153.569427
minLong = 137.945578

# Greater brisbane coordinates
# maxLat = brisBounds[3] #-26.35
# minLat = brisBounds[1] #-28.4
# maxLong = brisBounds[2] #153.55
# minLong = brisBounds[0] #152.5

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

lat = dataArray[:, 0]
long = dataArray[:, 1]
freq = dataArray[:, 2]
pts = 10_000


# Comment or uncomment depending on if you want to zoom into brisbane
[x, y] = np.meshgrid(np.linspace(minLong, maxLong, int(np.sqrt(pts))),
                     np.linspace(minLat, maxLat, int(np.sqrt(pts))))

z = griddata((long, lat), freq, (x, y), method='cubic', fill_value=50)
# z = Rbf(long, lat, freq, function='cubic')(x, y)

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
ax = gplt.polyplot(qld, ax=ax)
patch = PolygonPatch(qld['geometry'][2], transform=ax.transData)
implt = ax.imshow(z, extent=[np.min(x), np.max(x), np.min(y), np.max(y)], origin='lower',
        cmap='gist_rainbow')
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

# add the ability to zoom:
ax.figure.canvas.toolbar.push_current()
zoom_func = zoom_factory(ax, base_scale=1.1)

tkinter.mainloop()