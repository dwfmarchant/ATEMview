
from PyQt5 import QtCore
from Utils import make_time_channel_grid, mask_time_channel_grid

class GridWorker(QtCore.QThread):

    finishedGrid = QtCore.pyqtSignal(dict, name='finishedGrid')

    def __init__(self, data, ch):
        super().__init__()
        self.tInds = data.times.index
        self.data = data
        self.ch = ch
        self.grdOpts = {'number_cells':256,
                        'method':"cubic"}
        self.mask_radius = 100.
        self.mask = None

    def __del__(self):
        self.wait()

    def make_grid(self, tInd):
        data_time = self.data.getTime(tInd)
        x_vector, y_vector, grid = make_time_channel_grid(data_time, self.ch, **self.grdOpts)
        grid, self.mask = mask_time_channel_grid(data_time, grid, x_vector, y_vector,
                                                 mask_radius=self.mask_radius, mask=self.mask)
        signal = {'ch':self.ch,
                  'tInd':tInd,
                  'x_vector':x_vector,
                  'y_vector':y_vector,
                  'grid':grid,
                  'number_cells':self.grdOpts['number_cells']}
        return signal

    def run(self):
        for ti in self.tInds:
            print("Gridding {}, tInd = {}".format(self.ch, ti))
            signal = self.make_grid(ti)
            self.finishedGrid.emit(signal)
