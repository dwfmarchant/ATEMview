
from InvTools.Utils import makeGrid, maskGrid
import numpy as np

def make_time_channel_grid(data_time, channel_name,
                           number_cells=256, method="cubic"):

    if data_time[channel_name].isnull().all():
        grid = []
        x_vector = np.r_[-1., 1.]
        y_vector = np.r_[-1., 1.]
    else:
        x_vector, y_vector, grid = makeGrid(data_time.x,
                                            data_time.y,
                                            data_time[channel_name],
                                            nc=number_cells,
                                            method=method)


    return x_vector, y_vector, grid

def mask_time_channel_grid(data_time, grid, x_vector, y_vector, mask_radius=100., mask=None):
    if mask is None:
        mask = ~maskGrid(data_time.x.values, data_time.y.values,
                         x_vector, y_vector, mask_radius)
    elif mask.shape != grid.shape:
        print("Warning: Mask and grid different shapes")
        mask = ~maskGrid(data_time.x.values, data_time.y.values,
                         x_vector, y_vector, mask_radius)

    grid[mask] = np.nan
    return grid, mask
