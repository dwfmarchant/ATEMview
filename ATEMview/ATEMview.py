
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import numpy as np

from LocWindow import LocWidget
from DecayWindow import DecayWidget

class ATEMviewer(object):
    """docstring for ATEMviewer"""

    selectedLocInd = -1

    def __init__(self, data):

        # Store data
        self.data = data
        self.locs = data.locs.copy()

        # Initial the Gui
        self.LocWindow = LocWidget(self)
        self.LocWindow.setAll(self.locs.x.values, self.locs.y.values)

        self.DecayWindow = DecayWidget(self)

        # Initialize the selection
        self.setSelectedLocInd(self.locs.iloc[0].name)
        
    def setSelectedLocInd(self, locInd):
        """ docstring """
        if (locInd == self.locs.index).any():
            self.selectedLocInd = locInd
            selectedLocation = self.locs.loc[locInd]
            selectedDecay = self.data.getLoc(locInd)

            self.LocWindow.setSel(selectedLocation.x, selectedLocation.y)
            self.DecayWindow.setDecay(selectedDecay)

    @QtCore.pyqtSlot(dict)
    def get_event(self, event):
        """ docstring """

        if event['name'] == 'locClicked':
            closestLoc = self.getClosestLoc(event['xdata'], event['ydata'])
            self.setSelectedLocInd(closestLoc)
        elif event['name'] == 'nextLocInd':
            self.setSelectedLocInd(self.selectedLocInd+1)
        elif event['name'] == 'prevLocInd':
            self.setSelectedLocInd(self.selectedLocInd-1)    

    def getClosestLoc(self, x, y):
        """ docstring """
        dx = self.locs.x - x
        dy = self.locs.y - y
        r = np.sqrt(dx**2 + dy**2)
        closestInd = r.argmin()
        return closestInd



# class ApplicationWindow(QMainWindow):
#     """ Docstring """
#     def __init__(self, data):
#         QMainWindow.__init__(self)

#         self.data = data

#         self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#         self.setWindowTitle("application main window")

#         self.main_widget = QWidget(self)

#         # l = QVBoxLayout(self.main_widget)
#         # locs = self.data[['locInd', 'x', 'y']].drop_duplicates()
#         # sc = LocsCanvas(locs, self.main_widget, width=5, height=4, dpi=100)
#         # toolbar = NavigationToolbar(sc, self)
#         # l.addWidget(toolbar)
#         # l.addWidget(sc)

#         self.main_widget.setFocus()
#         self.setCentralWidget(self.main_widget)

#         self.statusBar().showMessage("Message", 2000)

if __name__ == '__main__':

    from InvTools.ATEM import ATEMdata

    obsFile = '/Users/dmarchant/Dropbox (CGI)/Projects2017/BlackwellHPX/Inv/20170425/Inv1_HMprelim/obs.txt'
    predFile = '/Users/dmarchant/Dropbox (CGI)/Projects2017/BlackwellHPX/Inv/20170425/Inv1_HMprelim/dpred.txt'

    dat = ATEMdata(obsFile, predFile)

    app = QApplication(sys.argv)
    ATEM = ATEMviewer(dat)

    # aw = ApplicationWindow(dat)
    # aw.setWindowTitle("PyQt5 Matplot Example")
    # aw.show()
    app.exec_()
