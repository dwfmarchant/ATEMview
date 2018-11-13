
from PyQt5 import QtCore
from .Utils import make_time_channel_grid, mask_time_channel_grid

class GridWorker(QtCore.QThread):

    finishedGrid = QtCore.pyqtSignal(dict, name='finishedGrid')

    def __init__(self, data, ch, moment=None):
        super().__init__()
        self.tInds = data.df[data.df.moment == moment].tInd.unique() if moment is not None else data.times.index
        self.data = data
        self.ch = ch
        self.moment = moment
        self.grdOpts = {'number_cells':256,
                        'method':"cubic"}
        self.mask_radius = 100.
        self.mask = None

    def __del__(self):
        self.wait()

    def make_grid(self, tInd):
        data_time = self.data.getTime(tInd)
        if self.moment is not None:
            data_time = data_time[data_time.moment == self.moment]
        x_vector, y_vector, grid = make_time_channel_grid(data_time, self.ch, **self.grdOpts)
        grid, self.mask = mask_time_channel_grid(data_time, grid, x_vector, y_vector,
                                                 mask_radius=self.mask_radius, mask=self.mask)

        signal = {'ch':self.ch,
                  'tInd':tInd,
                  'x_vector':x_vector,
                  'y_vector':y_vector,
                  'grid':grid,
                  'number_cells':self.grdOpts['number_cells']}

        if self.moment is not None:
            signal['moment'] = self.moment

        return signal

    def run(self):
        for ti in self.tInds:
            # print("Gridding {}, tInd = {}".format(self.ch, ti))
            signal = self.make_grid(ti)
            self.finishedGrid.emit(signal)
