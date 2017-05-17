
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Canvas import Canvas
from ATEMWidget import ATEMWidget

class LocWidget(ATEMWidget):
    """docstring for LocWidget"""

    def __init__(self, parent):
        super(LocWidget, self).__init__(parent)
        self.parent = parent
        self.init_ui()
        self.show()

    def init_ui(self):
        """ Docstring """
        self.canvas = Canvas(parent=self, width=5, height=4, dpi=100)
        self.selPlot, = self.canvas.axes.plot([], [], 'o', c='r', ms=2.)
        self.allPlot, = self.canvas.axes.plot([], [], 'o', c='k', ms=1.)
        self.selCrossX, = self.canvas.axes.plot([], [], '--', c='r', lw=0.5, zorder=0)
        self.selCrossY, = self.canvas.axes.plot([], [], '--', c='r', lw=0.5, zorder=0)
        self.canvas.axes.set_aspect('equal')
        self.canvas.canvasClicked.connect(self.canvasClicked)

        toolbar = NavigationToolbar(self.canvas, self, coordinates=False)
        l = QtWidgets.QVBoxLayout(self)
        l.addWidget(self.canvas)
        l.addWidget(toolbar)

    @QtCore.pyqtSlot(dict)
    def canvasClicked(self, event):
        signal = {'name':'closestLoc',
                  'x':event['xdata'],
                  'y':event['ydata']}
        self.ChangeSelectionSignal.emit(signal)

    def setAll(self, x, y):
        """ Docstring """
        self.allPlot.set_data(x, y)
        self.canvas.axes.set_xlim(x.min()-100., x.max()+100.)
        self.canvas.axes.set_ylim(y.min()-100., y.max()+100.)
        self.canvas.draw()

    def setLocation(self, loc):
        """ Docstring """
        x = loc.iloc[0].x
        y = loc.iloc[0].y
        self.selPlot.set_data(x, y)
        self.selCrossX.set_data(self.canvas.axes.get_xlim(),[y,y])
        self.selCrossY.set_data([x,x],self.canvas.axes.get_ylim())
        self.canvas.draw()

