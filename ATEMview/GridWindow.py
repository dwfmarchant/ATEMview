
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QVBoxLayout, QSlider
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from ATEMWidget import ATEMWidget

class GridCanvas(FigureCanvas):
    """ Docstring """

    locClicked = pyqtSignal(dict, name='locClicked')

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """ Docstring """

        # self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig = Figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        imshowOpts = {'origin':'lower',
                      'cmap':'jet',
                      'interpolation':'bilinear'}

        self.obs_axes = self.fig.add_subplot(121, aspect='equal')
        self.obs_im = self.obs_axes.imshow([[0.]], **imshowOpts)
        self.fig.colorbar(self.obs_im)

        self.pred_axes = self.fig.add_subplot(122, aspect='equal')
        self.pred_im = self.pred_axes.imshow([[0.]], **imshowOpts)
        self.fig.colorbar(self.pred_im)

        self.mpl_connect('button_press_event', self.onClick)

        self.draw()

    def showGrid(self, xv, yv, GrdObs, GrdPred):
        """Docstring"""

        vmin = np.nanmin(GrdObs)
        vmax = np.nanmax(GrdObs)

        self.obs_im.set_data(GrdObs)
        self.obs_im.set_extent((xv[0], xv[-1], yv[0], yv[-1]))
        self.obs_im.set_clim(vmin, vmax)


        self.pred_im.set_data(GrdPred)
        self.pred_im.set_extent((xv[0], xv[-1], yv[0], yv[-1]))
        self.pred_im.set_clim(vmin, vmax)

        self.draw()

    def onClick(self, event):
        """ Docstring """
        if event.inaxes is not None:
            signal = {'name':'locClicked',
                      'xdata':event.xdata,
                      'ydata':event.ydata}
            self.locClicked.emit(signal)

    def setClim(self, minVal, maxVal):
        self.obs_im.set_clim(minVal, maxVal)
        self.pred_im.set_clim(minVal, maxVal)
        self.draw()

class GridWidget(ATEMWidget):
    """docstring for GridWidget"""

    def __init__(self, parent):
        super(GridWidget, self).__init__(parent)
        self.parent = parent
        self.init_ui()
        self.init_signals()
        self.show()

    def init_ui(self):
        """ Docstring """
        self.gc = GridCanvas(parent=self, width=10, height=4, dpi=100)
        toolbar = NavigationToolbar(self.gc, self, coordinates=False)


        self.highSlider = QSlider(Qt.Horizontal)
        self.highSlider.setMaximum(100)
        self.highSlider.setValue(100)
        self.highSlider.valueChanged.connect(self.setClim)

        self.lowSlider = QSlider(Qt.Horizontal)
        self.lowSlider.setMaximum(100)
        self.lowSlider.setValue(0)
        self.lowSlider.valueChanged.connect(self.setClim)

        l = QVBoxLayout(self)
        l.addWidget(self.gc)
        l.addWidget(toolbar)
        l.addWidget(self.highSlider)
        l.addWidget(self.lowSlider)

    def init_signals(self):
        self.gc.locClicked.connect(self.parent.get_event)

    def setClim(self):
        lsVal = self.lowSlider.value()
        hsVal = self.highSlider.value()
        if lsVal>=hsVal:
            self.lowSlider.setValue(hsVal-1)
            lsVal = self.lowSlider.value()

        dv = self.absMaxValue-self.absMinValue
        self.gc.setClim(self.absMinValue+dv*lsVal/100., self.absMinValue+dv*hsVal/100.,)

    def setGrid(self, xv, yv, GrdObs, GrdPred):
        self.gc.showGrid(xv, yv, GrdObs, GrdPred)
        self.absMinValue = np.nanmin(GrdObs)
        self.absMaxValue = np.nanmax(GrdObs)
        self.setClim()

