import tkinter as tk
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
#import geoplot as gplt
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
#from descartes import PolygonPatch

#from scipy.interpolate import griddata
#from scipy.interpolate import Rbf
#from shapely.geometry import Point
import matplotlib.animation as animation
#from os.path import dirname, join

# My imports
from readFuncs import threaded_read_day, read_gps, read_hour, get_pmu_date
from zoom_factory import zoom_factory
from panFactory import panFactory
#from reset_detail import reset_detail_factory

import datetime
import matplotlib.dates as mdates

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
#    'X1064388-A', # noisy data
#    'X18755-E', # noisy data
    'X412017',
    'X831-O',
    'X34249-F',
    'X414042',
    'X4460-K',
    'X742845',
    'X756850', # originally commented out, also dips at 00:40:13
    'X410035',
    'X2189666',
    'X18524-B',
    'X94855-A', # originally commented out, also dips 00:40:13
    'X22116-D',
    'X2264432', # oscillations
    'X2264597',
    'X841621',
    'X467127',
    'X71950-A',
    'X61106-C'
]

# Whether or not to use the pmus from the above list
USE_PREDEFINED_PMUS = False

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
# For the plot on the left.
#MAX_ARRAY_LENGTH = 50 * 60
MAX_ARRAY_LENGTH = 100

class DataManager:
    def __init__(self):
        self.pmuList = []

    def readPmuData(self, dirPath, hour):
        if not self.pmuList:
            raise Exception('GPS data has not been read yet')
        #year, month, day = get_pmu_date(dirPath, pmu_name)
        yearMonthDay = {}
        self.pmuData = read_hour(dirPath, self.pmuList, hour, TIMESTAMP_COL, FREQ_COL, yearMonthDay)
        self.year = int(yearMonthDay['year'])
        self.month = int(yearMonthDay['month'])
        self.day = int(yearMonthDay['day'])
        self.pmuData.columns = self.pmuData.columns.str.lower()

    def readGpsData(self, path):
        self.gpsData = read_gps(path)
        self.gpsData.index = self.gpsData.index.str.lower()
        # comment/uncomment this:
        if USE_PREDEFINED_PMUS:
            self.pmuList = self.gpsData.index.tolist()

    def prepareData(self, time: datetime.datetime):
        self.relevantGpsData = self.gpsData.loc[self.pmuData.columns.tolist(), :]
        #self.timestamp = self.pmuData.index[0]
        self.timestamp = np.datetime64(time)
        self.freq = self.pmuData.loc[self.timestamp, :]
        self.freq.name = 'Frequency'
        self.timesliceData = pd.concat([self.relevantGpsData, self.freq], axis=1)
        self.timesliceDataArr = self.timesliceData.to_numpy()
        self.long = self.timesliceDataArr[:, 0]
        self.lat = self.timesliceDataArr[:, 1]
        self.freq = self.timesliceDataArr[:, 2]
        
        self.runningTimestamps = np.array([self.timestamp])
        self.runningFrequencies = np.array([self.freq])
        print(self.runningTimestamps)
        print(self.runningFrequencies)


        # self.runningData = np.concatenate(([self.timestamp], self.freq), axis=0)
        # self.runningData = np.reshape(self.runningData, (1, -1))
        # print('starting to set index 50 times')
        # for i in range(1, 51):
        #     self.setNewIndex(i)
        # print('finished setting index 50 times')
        # print(self.runningData)

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

        self.timestamp = self.pmuData.index[index]
        # timeslice = np.reshape(np.concatenate(([self.timestamp], self.freq), axis=0), (1, -1))
        # self.runningData = np.concatenate((self.runningData, timeslice), axis=1)
        # print('running data')
        # print(self.runningData)
        offset = 0 if np.size(self.runningTimestamps) < MAX_ARRAY_LENGTH else 1
        self.runningTimestamps = np.append(self.runningTimestamps[offset:], self.timestamp)
        self.runningFrequencies = np.vstack([self.runningFrequencies[offset:, :], self.freq])

    def setNewTime(self, time: datetime.datetime):
        self.timestamp = np.datetime64(time)
        #self.timestamp = pd.Timestamp(time)
        self.freq = self.pmuData.loc[self.timestamp, :]
        self.timesliceData = pd.concat([self.relevantGpsData, self.freq], axis=1)
        self.timesliceDataArr = self.timesliceData.to_numpy()
        self.freq = self.timesliceDataArr[:, 2]
        self.runningTimestamps = np.array([self.timestamp])
        self.runningFrequencies = np.array([self.freq])

    def incrementTime(self):
        self.timestamp += np.timedelta64(20, 'ms')
        #self.timestamp += pd.Timedelta(20, ms)
        self.freq = self.pmuData.loc[self.timestamp, :]
        self.timesliceData = pd.concat([self.relevantGpsData, self.freq], axis=1)
        self.timesliceDataArr = self.timesliceData.to_numpy()
        self.freq = self.timesliceDataArr[:, 2]

        offset = 0 if np.size(self.runningTimestamps) < MAX_ARRAY_LENGTH else 1
        self.runningTimestamps = np.append(self.runningTimestamps[offset:], self.timestamp)
        self.runningFrequencies = np.vstack([self.runningFrequencies[offset:, :], self.freq])
        


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title('Queensland Grid Visualisation')
        self.aus = gpd.read_file('australiaMap/STE_2021_AUST_GDA2020.shp')
        self.qld = self.aus[self.aus.STE_NAME21=='Queensland']
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(1, 2, 1)
        self.ax2 = self.fig.add_subplot(1, 2, 2)
        self.ax2.set_facecolor('#68D9FF')
        # self.ax = gplt.polyplot(self.qld, ax=self.ax)
        self.qld.plot(ax=self.ax2, facecolor='white', edgecolor='black', linewidth=0.2)

        self.animIndex = 0
        self.started = False
        self.timer = datetime.datetime(2021, 7, 28, 0, 0, 0, 0)
        self.timeSet = False

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        #self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        #self.toolbar.update()
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
        self.timeFrame = tk.Frame(self)
        self.timeLabel = tk.Label(self, text='Time not specified', font=('Arial', 15))
        self.playPauseBtn = tk.Button(self, text='Pause', command=self._playPause)

        self.setTimeFrame = tk.Frame(self)
        self.setTimeLabel = tk.Label(self, text='   Set Time: ')
        self.setHour = tk.Spinbox(self, from_=0, to=23, wrap=True, width=3, format='%02.0f')
        self.hourMinSep = tk.Label(self, text=':')
        self.setMin = tk.Spinbox(self, from_=0, to=59, wrap=True, width=3, format='%02.0f')
        self.minSecSep = tk.Label(self, text=':')
        self.setSec = tk.Spinbox(self, from_=0, to=59, wrap=True, width=3, format='%02.0f')
        self.secDecPoint = tk.Label(self, text='.')
        self.setHundredths = tk.Spinbox(self, from_=0, to=95, increment=2, wrap=True, width=3, format='%02.0f')
        self.setTimeBtn = tk.Button(self, text='Set', command=self._setTime)

        self._pmuDirPath = ''
        self._gpsFilePath = ''

        self.dataManager = DataManager()
        self.dataManager.pmuList = pmus

        self._packInit()

        # https://stackoverflow.com/questions/6299943/how-do-i-animate-the-ticks-on-the-x-axis
        #self.bg1 = self.canvas.copy_from_bbox()

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

        self.timeLabel.pack(in_=self.timeFrame, side=tk.LEFT)
        self.playPauseBtn.pack(in_=self.timeFrame, side=tk.LEFT)

        self.setTimeLabel.pack(in_=self.setTimeFrame, side=tk.LEFT)
        self.setHour.pack(in_=self.setTimeFrame, side=tk.LEFT)
        self.hourMinSep.pack(in_=self.setTimeFrame, side=tk.LEFT)
        self.setMin.pack(in_=self.setTimeFrame, side=tk.LEFT)
        self.minSecSep.pack(in_=self.setTimeFrame, side=tk.LEFT)
        self.setSec.pack(in_=self.setTimeFrame, side=tk.LEFT)
        self.secDecPoint.pack(in_=self.setTimeFrame, side=tk.LEFT)
        self.setHundredths.pack(in_=self.setTimeFrame, side=tk.LEFT)
        self.setTimeBtn.pack(in_=self.setTimeFrame, side=tk.LEFT)
        self.setTimeFrame.pack(in_=self.timeFrame, side=tk.LEFT)

        self.timeFrame.pack(side=tk.TOP)
        #self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def setupAx1(self):
        # self.linePlots = []
        #x = self.dataManager.runningData[:, 0]
        x = self.dataManager.runningTimestamps
        # for i in range(1, np.size(self.dataManager.runningData, axis=0) + 1):
        #     self.linePlots.append(self.ax1.plot(x, self.dataManager.runningData[:, i]))
        # #self.linePlot = self.ax1.plot()
        # self.canvas.draw()

        #y = self.dataManager.runningData[:, 1:]
        y = self.dataManager.runningFrequencies
        self.lines = self.ax1.plot(x, y)

        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))
        self.ax1.legend(self.dataManager.relevantGpsData.index.tolist(), loc='upper left')

        self.canvas.draw()
        
        print('x')
        print(x)
        print('y')
        print(y)
        #exit()

        #self.anim1 = animation.FuncAnimation(self.fig, self.animateAx1, interval)

    def setupAx2(self):
        hour = self.setHour.get()
        self.dataManager.readGpsData(self._gpsFilePath)
        self.dataManager.readPmuData(self._pmuDirPath, hour)
        self.timer = datetime.datetime(
            self.dataManager.year,
            self.dataManager.month,
            self.dataManager.day,
            int(self.setHour.get()),
            int(self.setMin.get()),
            int(self.setSec.get()),
            int(self.setHundredths.get()) * 10_000
        )
        self.dataManager.prepareData(self.timer)
        

        pointSizes = (self.dataManager.freq - self.dataManager.minFreq) / self.dataManager.freqRange * SIZE_RANGE + MIN_SIZE
        self.scatterplt = self.ax2.scatter(self.dataManager.long, self.dataManager.lat, s=pointSizes, c=self.dataManager.freq, alpha=0.7,
                zorder=20, cmap='gist_rainbow', vmin=self.dataManager.freq5thPercent, vmax=self.dataManager.freq95thPercent)
        self.fig.colorbar(self.scatterplt, label='Frequency (Hz)', ax=self.ax2)
        plt.xlabel('Longitude (°)')
        plt.ylabel('Latitude (°)')
        self.canvas.draw()

        # self.anim = animation.FuncAnimation(self.fig, self.animateAx2, interval=50, blit=True)

        #self.ax2.figure.canvas.toolbar.push_current()
        zoom_func = zoom_factory(self.ax2, base_scale=1.1)
        panFunc = panFactory(self.ax2)

    def setupPlots(self):
        self.setupAx2()
        self.setupAx1()

        self.anim = animation.FuncAnimation(self.fig, self.animate, interval=50, blit=False)
        self.started = True

    def animateAx1(self, i):
        i = 0
        x = self.dataManager.runningTimestamps
        for plot in self.lines:
            plot.set_data(x, self.dataManager.runningFrequencies[:, i].flatten())
            i += 1

        # if self.animIndex % 50 == 0:
        #     self.ax1.relim()
        #     self.ax1.autoscale_view()
        self.ax1.relim()
        self.ax1.autoscale_view()

    def animateAx2(self, i):
        self.animIndex += 1
        #self.dataManager.setNewIndex(self.animIndex)
        self.dataManager.incrementTime()
        pointSizes = (self.dataManager.freq - self.dataManager.minFreq) / self.dataManager.freqRange * SIZE_RANGE + MIN_SIZE
        self.scatterplt.set_sizes(pointSizes)
        self.scatterplt.set_array(self.dataManager.freq)

        # TODO: make this not hard coded
        self.timer += datetime.timedelta(0, 0, 1e6 // 50) # add 0.02 seconds
        timeStr = self.timer.strftime('24hr time: %H:%M:%S.%f')
        self.timeLabel.config(text=timeStr)

        return self.scatterplt,
        
    def animate(self, i):
        self.animateAx2(i)
        self.animateAx1(i)

        # This should flatten the tuple
        # https://stackoverflow.com/questions/10632839/transform-list-of-tuples-into-a-flat-list-or-a-matrix/35228431
        # return list(sum([self.scatterplt, list(self.lines)], ()))

        return [self.scatterplt] + self.lines
        #return self.scatterplt,

    def _selectPmu(self):
        self._pmuDirPath = filedialog.askdirectory()
        self.pmuDir.config(text=self._pmuDirPath)
        if self._pmuDirPath and self._gpsFilePath and self.timeSet:
            self.setupPlots()

    def _selectGps(self):
        self._gpsFilePath = filedialog.askopenfilename()
        self.gpsFile.config(text=self._gpsFilePath)
        if self._pmuDirPath and self._gpsFilePath and self.timeSet:
            self.setupPlots()

    def _playPause(self):
        if not self.started:
            return
        if self.playPauseBtn['text'] == 'Pause':
            self.playPauseBtn.config(text='Play')
            self.anim.pause()
        else:
            self.playPauseBtn.config(text='Pause')
            self.anim.resume()

    def _setTime(self):
        hour = int(self.setHour.get())
        min = int(self.setMin.get())
        sec = int(self.setSec.get())
        hundredths = int(self.setHundredths.get())
        self.timer = datetime.datetime(2021, 7, 28, hour, min, sec, hundredths * 10_000)
        
        self.timeSet = True
        if self.started:
            self.dataManager.setNewTime(self.timer)
        elif self._pmuDirPath and self._gpsFilePath and self.timeSet:
            self.setupPlots()
        #print(f'{hour:02d}:{min:02d}:{sec:02d}.{hundredths:02d}')


if __name__ == '__main__':
    app = App()
    app.mainloop()
