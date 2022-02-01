import tkinter as tk
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
import geoplot as gplt
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from descartes import PolygonPatch

from scipy.interpolate import griddata
from scipy.interpolate import Rbf
#from shapely.geometry import Point
import matplotlib.animation as animation
from os.path import dirname, join

# My imports
from readFuncs import threaded_read_day, read_gps, read_hour
from zoom_factory import zoom_factory
from reset_detail import reset_detail_factory

import datetime

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

# gps_data = read_gps('D:\\PMU\\PMU_GPS.xlsx')
# hour_data = read_hour('D:\\PMU\\2021\\07\\28', pmus, '00', 0, 3)

# hour_data.columns = hour_data.columns.str.lower()
# gps_data.index = gps_data.index.str.lower()

# # print(hour_data)
# # print(gps_data)
# # print(gps_data.loc[hour_data.columns.tolist(), :])

# relevant_gps_data = gps_data.loc[hour_data.columns.tolist(), :]
# timestamp = hour_data.index[0]
# freq = hour_data.loc[timestamp, :]
# freq.name = 'Frequency'
# print(freq)

# timeslice_data = pd.concat([relevant_gps_data, freq], axis=1)
# print(timeslice_data)
# timeslice_data_arr = timeslice_data.to_numpy()
# print(timeslice_data_arr)


# long = timeslice_data_arr[:, 0]
# lat = timeslice_data_arr[:, 1]
# freq = timeslice_data_arr[:, 2]
# pts = 10_000

# Queensland coordinates
maxLat = -9.942333
minLat = -29.184142
maxLong = 153.569427
minLong = 137.945578

# [x, y] = np.meshgrid(np.linspace(minLong, maxLong, int(np.sqrt(pts))),
#                      np.linspace(minLat, maxLat, int(np.sqrt(pts))))

# z = griddata((long, lat), freq, (x, y), method='cubic', fill_value=50)

# print('Completed extracting data')


# # ================ Map stuff ==================

# australia = gpd.read_file('australiaMap/STE_2021_AUST_GDA2020.shp')
# qld = australia[australia.STE_NAME21=='Queensland']
# maxLat = -9.942333
# minLat = -29.184142
# maxLong = 153.569427
# minLong = 137.945578

# ================ Tkinter stuff ==================

TIMESTAMP_COL = 0
FREQ_COL = 3

# For the points in the scatterplot
MAX_SIZE = 200
MIN_SIZE = 20
SIZE_RANGE = MAX_SIZE - MIN_SIZE

class DataManager:
    def __init__(self):
        self.pmuList = []

    def readPmuData(self, dirPath):
        if not self.pmuList:
            raise Exception('GPS data has not been read yet')
        self.pmuData = read_hour(dirPath, self.pmuList, '00', TIMESTAMP_COL, FREQ_COL)
        self.pmuData.columns = self.pmuData.columns.str.lower()

    def readGpsData(self, path):
        self.gpsData = read_gps(path)
        self.gpsData.index = self.gpsData.index.str.lower()
        # self.pmuList = self.gpsData.index.tolist()

    def prepareData(self):
        self.relevantGpsData = self.gpsData.loc[self.pmuData.columns.tolist(), :]
        self.timestamp = self.pmuData.index[0]
        self.freq = self.pmuData.loc[self.timestamp, :]
        self.freq.name = 'Frequency'
        self.timesliceData = pd.concat([self.relevantGpsData, self.freq], axis=1)
        self.timesliceDataArr = self.timesliceData.to_numpy()
        self.long = self.timesliceDataArr[:, 0]
        self.lat = self.timesliceDataArr[:, 1]
        self.freq = self.timesliceDataArr[:, 2]
        print('before min/max')
        pmuDataArr = self.pmuData.to_numpy()
        print(pmuDataArr)
        self.maxFreq = np.nanmax(pmuDataArr)
        self.minFreq = np.nanmin(pmuDataArr)
        self.freq5thPercent = np.nanpercentile(pmuDataArr, 5)
        self.freq95thPercent = np.nanpercentile(pmuDataArr, 95)
        self.freqRange = self.maxFreq - self.minFreq
        print(f'Max freqency: {self.maxFreq}')
        print(f'Min frequency: {self.minFreq}')
        print('Completed extracting data')

    def setNewIndex(self, index):
        # Can probably call this within the prepareData function to avoid code duplication
        self.freq = self.pmuData.iloc[index, :]
        self.freq.name = 'Frequency'
        self.timesliceData = pd.concat([self.relevantGpsData, self.freq], axis=1)
        self.timesliceDataArr = self.timesliceData.to_numpy()
        self.freq = self.timesliceDataArr[:, 2]


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title('Queensland Grid Visualisation')
        self.aus = gpd.read_file('australiaMap/STE_2021_AUST_GDA2020.shp')
        self.qld = self.aus[self.aus.STE_NAME21=='Queensland']
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax = gplt.polyplot(self.qld, ax=self.ax)

        self.animIndex = 0
        self.timer = datetime.datetime(2021, 7, 28, 0, 0, 0, 0)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        self.canvas.mpl_connect('key_press_event', key_press_handler)

        self.btnFrame = tk.Frame(self)
        self.filesFrame = tk.Frame(self)
        self.pmuFrame = tk.Frame(self)
        self.gpsFrame = tk.Frame(self)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.pmuSelectButton = tk.Button(self, text='Select PMU data folder', command=self._selectPmu)
        self.gpsSelectButton = tk.Button(self, text='Select GPS location spreadsheet', command=self._selectGps)
        self.pmuDir = tk.Label(self, text='No PMU folder selected')
        self.gpsFile = tk.Label(self, text='No GPS location spreadsheet selected')
        self.timeLabel = tk.Label(self, text='Time not specified')

        self._pmuDirPath = ''
        self._gpsFilePath = ''

        self.dataManager = DataManager()
        self.dataManager.pmuList = pmus

        self._packInit()

    def _packInit(self):
        self.quitButton.pack(in_=self.btnFrame, side=tk.RIGHT, anchor='w')

        self.pmuSelectButton.pack(in_=self.pmuFrame, side=tk.LEFT)
        self.pmuDir.pack(in_=self.pmuFrame, side=tk.LEFT)
        self.gpsSelectButton.pack(in_=self.gpsFrame, side=tk.LEFT)
        self.gpsFile.pack(in_=self.gpsFrame, side=tk.LEFT)
        self.pmuFrame.pack(in_=self.filesFrame, side=tk.TOP, fill=tk.X)
        self.gpsFrame.pack(in_=self.filesFrame, side=tk.TOP, fill=tk.X)
        self.filesFrame.pack(in_=self.btnFrame, side=tk.LEFT)

        self.btnFrame.pack(side=tk.TOP, fill=tk.X)
        self.timeLabel.pack(side=tk.TOP)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def setupPlots(self):
        self.dataManager.readPmuData(self._pmuDirPath)
        self.dataManager.readGpsData(self._gpsFilePath)
        self.dataManager.prepareData()

        pointSizes = (self.dataManager.freq - self.dataManager.minFreq) / self.dataManager.freqRange * SIZE_RANGE + MIN_SIZE
        self.scatterplt = self.ax.scatter(self.dataManager.long, self.dataManager.lat, s=pointSizes, c=self.dataManager.freq, alpha=0.7,
                zorder=20, cmap='gist_rainbow', vmin=self.dataManager.freq5thPercent, vmax=self.dataManager.freq95thPercent)
        self.fig.colorbar(self.scatterplt, label='Frequency (Hz)', ax=self.ax)
        plt.xlabel('Longitude (°)')
        plt.ylabel('Latitude (°)')
        self.canvas.draw()

        self.ani = animation.FuncAnimation(self.fig, self.animatePlot, interval=50, blit=True)

        self.ax.figure.canvas.toolbar.push_current()
        zoom_func = zoom_factory(self.ax, base_scale=1.1)

    def animatePlot(self, i):
        self.animIndex += 1
        self.dataManager.setNewIndex(self.animIndex)
        pointSizes = (self.dataManager.freq - self.dataManager.minFreq) / self.dataManager.freqRange * SIZE_RANGE + MIN_SIZE
        self.scatterplt.set_sizes(pointSizes)
        self.scatterplt.set_array(self.dataManager.freq)

        # TODO: make this not hard coded
        self.timer += datetime.timedelta(0, 0, 1e6 // 50) # add 0.02 seconds
        timeStr = self.timer.strftime('24hr time: %H:%M:%S.%f')
        self.timeLabel.config(text=timeStr)

        return self.scatterplt,
        

    def _selectPmu(self):
        self._pmuDirPath = filedialog.askdirectory()
        self.pmuDir.config(text=self._pmuDirPath)
        if self._pmuDirPath and self._gpsFilePath:
            self.setupPlots()

    def _selectGps(self):
        self._gpsFilePath = filedialog.askopenfilename()
        self.gpsFile.config(text=self._gpsFilePath)
        if self._pmuDirPath and self._gpsFilePath:
            self.setupPlots()


if __name__ == '__main__':
    app = App()
    app.mainloop()

exit()

root = tk.Tk()
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

button_quit = tk.Button(master=root, text='Quit', command=root.quit)

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
button_quit.pack(side=tk.BOTTOM)
#slider_update.pack(side=tk.BOTTOM)
toolbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

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

tk.mainloop()