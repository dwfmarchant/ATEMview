
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import numpy as np
from InvTools.Utils import makeGrid, maskGrid

from MainWindow import MainWindow
from DataLoadDialog import DataLoadDialog
from LocWindow import LocWidget
from DecayWindow import DecayWidget
from GridWindow import GridWidget

class ATEMviewer(object):
    """ docstring for ATEMviewer """

    selectedLocInd = -1
    selectedTimeInd = -1

    LocWindow = None
    DecayWindow = None
    GridWindow = None
    grids = {}

    def __init__(self, data=None):

        # Launch the loader
        if data is None:
            dataLoader = DataLoadDialog()
            dataLoader.exec_()
            self.data = dataLoader.data
        else:
            self.data = data

        # Initialize the Gui
        self.MainWindow = MainWindow(self)

        # Initialize the selection
        self.setSelectedLocInd(self.data.locs.iloc[0].name)
        self.setSelectedTimeInd(self.data.times.iloc[0].name)

    def openLocWindow(self):
        """ docstring """
        if self.LocWindow is None:
            self.LocWindow = LocWidget(self)
            self.LocWindow.setAll(self.data.locs.x.values,
                                  self.data.locs.y.values)
            self.setSelectedLocInd(self.selectedLocInd)
            self.setSelectedTimeInd(self.selectedTimeInd)
        else:
            self.LocWindow.toggleVisible()

    def openDecayWindow(self):
        """ docstring """
        if self.DecayWindow is None:
            self.DecayWindow = DecayWidget(self)
            self.setSelectedLocInd(self.selectedLocInd)
            self.setSelectedTimeInd(self.selectedTimeInd)
        else:
            self.DecayWindow.toggleVisible()

    def openGridWindow(self):
        """ docstring """
        if self.GridWindow is None:
            self.GridWindow = GridWidget(self)
            self.setSelectedLocInd(self.selectedLocInd)
            self.setSelectedTimeInd(self.selectedTimeInd)
        else:
            self.GridWindow.toggleVisible()

    def setSelectedLocInd(self, locInd):
        """ docstring """
        if locInd in self.data.locs.index:
            self.selectedLocInd = locInd
            selectedLocation = self.data.locs.loc[locInd]
            selectedDecay = self.data.getLoc(locInd)

            if self.LocWindow is not None:
                self.LocWindow.setSel(selectedLocation.x, selectedLocation.y)
            if self.DecayWindow is not None:
                self.DecayWindow.setDecay(selectedDecay)

    def setSelectedTimeInd(self, timeInd):
        """ docstring """

        if timeInd in self.data.times.index:
            self.selectedTimeInd = timeInd
            if self.GridWindow is not None:
                if timeInd not in self.grids:
                    dt = self.data.getTime(timeInd)
                    xv, yv, GrdObs = makeGrid(dt.x, dt.y, dt.dBdt_Z, nc=256, method="cubic")
                    _, _, GrdPred = makeGrid(dt.x, dt.y, dt.dBdt_Z_pred, nc=256, method="cubic")
                    mask = ~maskGrid(dt.x.values, dt.y.values, xv, yv, 100.)
                    GrdObs[mask] = np.nan
                    GrdPred[mask] = np.nan
                    self.grids[timeInd] = [xv, yv, GrdObs, GrdPred]
                self.GridWindow.setGrid(*self.grids[timeInd])

    def closeAll(self):
        """ Close all open windows """
        for window in [self.LocWindow, self.DecayWindow, self.GridWindow]:
            if window is not None:
                window.deleteLater()
                window = None
        self.MainWindow.close()

    @QtCore.pyqtSlot(dict)
    def get_event(self, event):
        """ docstring """

        if event['name'] == 'locClicked':
            closestLoc = self.getClosestLoc(event['xdata'], event['ydata'])
            self.setSelectedLocInd(closestLoc)
        elif event['name'] == 'nextLocInd':
            self.setSelectedLocInd(self.selectedLocInd + 1)
        elif event['name'] == 'prevLocInd':
            self.setSelectedLocInd(self.selectedLocInd - 1)
        elif event['name'] == 'nextTimeInd':
            self.setSelectedTimeInd(self.selectedTimeInd + 1)
        elif event['name'] == 'prevTimeInd':
            self.setSelectedTimeInd(self.selectedTimeInd - 1)
        else:
            print(event['name'])


    def getClosestLoc(self, x, y):
        """ docstring """
        dx = self.data.locs.x - x
        dy = self.data.locs.y - y
        r = np.sqrt(dx**2 + dy**2)
        closestInd = r.argmin()
        return closestInd

if __name__ == '__main__':

    from InvTools.ATEM import ATEMdata

    app = QApplication(sys.argv)
    ATEM = ATEMviewer()
    app.exec_()
