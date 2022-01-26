import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

data = np.loadtxt('Madagascar_Elevation.txt')
long = data[:, 0]
lat = data[:, 1]
elev = data[:, 2]
pts = 1_000_000
[x, y] = np.meshgrid(np.linspace(np.min(long), np.max(long), int(np.sqrt(pts))),
                     np.linspace(np.min(lat), np.max(lat), int(np.sqrt(pts))))

z = griddata((long, lat), elev, (x, y), method='linear')
x = np.matrix.flatten(x)
y = np.matrix.flatten(y)
z = np.matrix.flatten(z)

plt.scatter(x, y, 1, z)
plt.colorbar(label='Elevation above sea level (m)')
plt.xlabel('Longitude (°)')
plt.ylabel('Latitude (°)')
plt.show()