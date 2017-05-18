
from InvTools.Utils import makeGrid, maskGrid
import numpy as np

def makeTimeChannelGrid(data_time, channel_name, number_cells=256, method="cubic", mask_radius=100., mask=None):

    x_vector, y_vector, grid = makeGrid(data_time.x,
                                        data_time.y,
                                        data_time[channel_name],
                                        nc=number_cells,
                                        method=method)
    if mask is None:
        mask = ~maskGrid(data_time.x.values, data_time.y.values,
                         x_vector, y_vector, mask_radius)
    grid[mask] = np.nan
    return x_vector, y_vector, grid, mask
