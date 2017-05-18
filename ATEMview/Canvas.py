
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Canvas(FigureCanvas):
    """docstring for Canvas"""

    canvasClicked = QtCore.pyqtSignal(dict, name='canvasClicked')

    def __init__(self, parent=None, width=5, height=4, dpi=100, share_ax=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, sharex=share_ax, sharey=share_ax)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.mpl_connect('button_press_event', self.onClick)
        self.draw()

    def onClick(self, event):
        """Docstring"""
        if event.inaxes is not None:
            signal = {'name':'CanvasClicked',
                      'xdata':event.xdata,
                      'ydata':event.ydata}
            self.canvasClicked.emit(signal)
