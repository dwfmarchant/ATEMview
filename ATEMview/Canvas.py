
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Canvas(FigureCanvas):
    """docstring for Canvas"""

    canvasClicked = QtCore.pyqtSignal(dict, name='canvasClicked')

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                                         QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.initPlot()
        self.mpl_connect('button_press_event', self.onClick)
        self.draw()

    def initPlot(self):
        """Docstring"""
        pass

    def onClick(self, event):
        """Docstring"""
        if event.inaxes is not None:
            signal = {'name':'CanvasClicked',
                      'xdata':event.xdata,
                      'ydata':event.ydata}
            self.canvasClicked.emit(signal)
