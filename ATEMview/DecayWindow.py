
import numpy as np
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Canvas import Canvas

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
        self.timePlot, = self.axes.plot([], [], '-', color='green', zorder = -1)
        self.axes.legend()

class DecayWidget(QWidget):
    """docstring for LocWidget"""
    def __init__(self, parent):
        super(DecayWidget, self).__init__()
        self.parent = parent
        self.init_ui()
        self.lc.locClicked.connect(parent.get_event)
        self.show()

    def init_ui(self):
        """ Docstring """
        self.lc = DecayCanvas(parent=self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.lc, self, coordinates=False)

        l = QVBoxLayout(self)
        l.addWidget(self.lc)
        l.addWidget(toolbar)

    def toggleVisible(self):
        """ docstring """
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def setLocation(self, loc):
        """ Docstring """

        t = loc.t.values
        obs = loc.dBdt_Z.values
        pred = loc.dBdt_Z_pred.values
        lower = obs - loc.dBdt_Z_uncert.values
        upper = obs + loc.dBdt_Z_uncert.values

        self.lc.obsPlot.set_data(t, obs)
        self.lc.predPlot.set_data(t, pred)

        tv = np.r_[t[0], t, t[-1], t[::-1], t[0]]
        v = np.r_[lower[0], upper, lower[-1], lower[::-1], lower[0]]
        self.lc.uncertBounds.set_paths([np.c_[tv, v]])

        self.lc.axes.set_xlim(t.min(), t.max())
        self.lc.axes.set_ylim(sounding.dBdt_Z.min(), sounding.dBdt_Z.max())
        self.lc.axes.set_title(sounding.locInd.iloc[0])
        self.lc.draw()

    def setTime(self, time):
        """ docstring """
        self.lc.timePlot.set_data([time, time], [1e-20, 10])
        self.lc.draw()
