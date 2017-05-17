
import numpy as np
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Canvas import Canvas
from ATEMWidget import ATEMWidget

class DecayCanvas(Canvas):
    """ Docstring """

    locClicked = pyqtSignal(dict, name='locClicked')

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """Docstring"""
        super().__init__(parent, width, height, dpi)
        self.axes.set_yscale('log')
        self.axes.set_xscale('log')

    def initPlot(self):
        """Docstring"""
        self.obsPlot, = self.axes.plot([], [], '-o', c='k', ms=2., label="Obs")
        self.predPlot, = self.axes.plot([], [], '-o', c='r', ms=2., label="Pred")
        self.uncertBounds = self.axes.fill_between([], [], alpha=0.3, color='k')
        self.timePlot, = self.axes.plot([], [], ':', color='green', zorder = -1)
        self.axes.legend()

class DecayWidget(ATEMWidget):
    """docstring for LocWidget"""
    def __init__(self, parent):
        super(DecayWidget, self).__init__(parent)
        self.parent = parent
        self.init_ui()
        self.init_signals()
        self.show()

    def init_ui(self):
        """ Docstring """
        self.dc = DecayCanvas(parent=self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.dc, self, coordinates=False)

        l = QVBoxLayout(self)
        l.addWidget(self.dc)
        l.addWidget(toolbar)

    def init_signals(self):
        self.dc.locClicked.connect(self.parent.get_event)

    def setLocation(self, loc):
        """ Docstring """

        t = loc.t.values
        obs = loc.dBdt_Z.values
        pred = loc.dBdt_Z_pred.values
        lower = obs - loc.dBdt_Z_uncert.values
        upper = obs + loc.dBdt_Z_uncert.values

        self.dc.obsPlot.set_data(t, obs)
        self.dc.predPlot.set_data(t, pred)

        tv = np.r_[t[0], t, t[-1], t[::-1], t[0]]
        v = np.r_[lower[0], upper, lower[-1], lower[::-1], lower[0]]
        self.dc.uncertBounds.set_paths([np.c_[tv, v]])

        self.dc.axes.set_xlim(t.min(), t.max())
        self.dc.axes.set_ylim(loc.dBdt_Z.min(), loc.dBdt_Z.max())
        self.dc.axes.set_title(loc.locInd.iloc[0])
        self.dc.draw()

    def setTime(self, time):
        """ docstring """
        self.dc.timePlot.set_data([time, time], [1e-20, 1e20])
        self.dc.draw()

