
import numpy as np
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Canvas import Canvas
from ATEMWidget import ATEMWidget

class DecayWidget(ATEMWidget):
    """docstring for LocWidget"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.init_signals()
        self.show()

    def init_ui(self):
        """ Docstring """
        self.canvas = Canvas(parent=self, width=5, height=4, dpi=100)
        self.obsPlot, = self.canvas.axes.plot([], [], '-o', c='k', ms=2., label="Obs")
        self.predPlot, = self.canvas.axes.plot([], [], '-o', c='r', ms=2., label="Pred")
        self.uncertBounds = self.canvas.axes.fill_between([], [], alpha=0.3, color='k')
        self.timePlot, = self.canvas.axes.plot([], [], ':', color='green', zorder = -1)
        self.canvas.axes.legend()
        self.canvas.axes.set_yscale('log')
        self.canvas.axes.set_xscale('log')

        toolbar = NavigationToolbar(self.canvas, self, coordinates=False)

        l = QtWidgets.QVBoxLayout(self)
        l.addWidget(self.canvas)
        l.addWidget(toolbar)

    def init_signals(self):
        self.canvas.canvasClicked.connect(self.canvasClicked)

    @QtCore.pyqtSlot(dict)
    def canvasClicked(self, event):
        signal = {'name':'closestTime',
                  't':event['xdata']}
        self.ChangeSelectionSignal.emit(signal)

    def setLocation(self, loc):
        """ Docstring """

        t = loc.t.values
        obs = loc.dBdt_Z.values
        pred = loc.dBdt_Z_pred.values
        lower = obs - loc.dBdt_Z_uncert.values
        upper = obs + loc.dBdt_Z_uncert.values

        self.obsPlot.set_data(t, obs)
        self.predPlot.set_data(t, pred)

        tv = np.r_[t[0], t, t[-1], t[::-1], t[0]]
        v = np.r_[lower[0], upper, lower[-1], lower[::-1], lower[0]]
        self.uncertBounds.set_paths([np.c_[tv, v]])

        self.canvas.axes.set_xlim(t.min(), t.max())
        self.canvas.axes.set_ylim(loc.dBdt_Z.min(), loc.dBdt_Z.max())
        self.canvas.axes.set_title(loc.locInd.iloc[0])
        self.canvas.draw()

    def setTime(self, time):
        """ docstring """
        self.timePlot.set_data([time, time], [1e-20, 1e20])
        self.canvas.draw()
