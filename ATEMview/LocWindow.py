
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Canvas import Canvas
from ATEMWidget import ATEMWidget

class LocsCanvas(Canvas):
    """ Docstring """

    locClicked = pyqtSignal(dict, name='locClicked')

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """Docstring"""
        super().__init__(parent, width, height, dpi)
        self.axes.set_aspect('equal')

    def initPlot(self):
        """Docstring"""
        self.selPlot, = self.axes.plot([], [], 'o', c='r', ms=2.)
        self.allPlot, = self.axes.plot([], [], 'o', c='k', ms=1.)
        self.selCrossX, = self.axes.plot([], [], '--', c='r', lw=0.5, zorder=0)
        self.selCrossY, = self.axes.plot([], [], '--', c='r', lw=0.5, zorder=0)

    def onClick(self, event):
        """ Docstring """

        if event.inaxes is not None:
            signal = {'name':'locClicked',
                      'xdata':event.xdata,
                      'ydata':event.ydata}
            self.locClicked.emit(signal)

class LocWidget(ATEMWidget):
    """docstring for LocWidget"""

    def __init__(self, parent):
        super(LocWidget, self).__init__(parent)
        self.parent = parent
        self.init_ui()
        self.init_signals()
        self.show()

    def init_ui(self):
        """ Docstring """
        self.lc = LocsCanvas(parent=self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.lc, self, coordinates=False)
        l = QVBoxLayout(self)
        l.addWidget(self.lc)
        l.addWidget(toolbar)

    def init_signals(self):
        self.lc.locClicked.connect(self.parent.get_event)

    def setAll(self, x, y):
        """ Docstring """
        self.lc.allPlot.set_data(x, y)
        self.lc.axes.set_xlim(x.min()-100., x.max()+100.)
        self.lc.axes.set_ylim(y.min()-100., y.max()+100.)
        self.lc.draw()

    def setLocation(self, loc):
        """ Docstring """
        x = loc.iloc[0].x
        y = loc.iloc[0].y
        self.lc.selPlot.set_data(x, y)
        self.lc.selCrossX.set_data(self.lc.axes.get_xlim(),[y,y])
        self.lc.selCrossY.set_data([x,x],self.lc.axes.get_ylim())
        self.lc.draw()

