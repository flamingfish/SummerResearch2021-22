import numpy as np
from scipy.interpolate import griddata

def reset_detail_factory(pts, long, lat, freq, implt):
    def reset_detail(xlim, ylim):
        global x, y, z
        [x, y] = np.meshgrid(np.linspace(xlim[0], xlim[1], int(np.sqrt(pts))),
                        np.linspace(ylim[0], ylim[1], int(np.sqrt(pts))))
        z = griddata((long, lat), freq, (x, y), method='cubic', fill_value=50)
        implt.set_data(z)
        implt.set_extent((np.min(x), np.max(x), np.min(y), np.max(y)))

        return x, y, z

    return reset_detail