
from PyQt5 import QtCore
import numpy as np
from Utils import makeTimeChannelGrid

class GridWorker(QtCore.QThread):

    finishedGrid = QtCore.pyqtSignal(dict, name='finishedGrid')

    def __init__(self, data, ch):
        super().__init__()
        self.tInds = data.times.index
        self.data = data
        self.ch = ch
        self.mask = None
        self.grdOpts = {'number_cells':256,
                        'method':"cubic",
                        'mask_radius':100.}

    def __del__(self):
        self.wait()

    def make_grid(self, tInd):
        data_time = self.data.getTime(tInd)
        x_vector, y_vector, grid, self.mask = makeTimeChannelGrid(data_time, self.ch,
                                                                  mask=self.mask, **self.grdOpts)
        signal = {'ch':self.ch,
                  'tInd':tInd,
                  'x_vector':x_vector,
                  'y_vector':y_vector,
                  'grid':grid}
        return signal

    def run(self):
        for ti in self.tInds:
            print("Gridding {}, tInd = {}".format(self.ch, ti))
            signal = self.make_grid(ti)
            self.finishedGrid.emit(signal)
