
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from ATEMWidget import ATEMWidget
from Canvas import Canvas

class GridWidget(ATEMWidget):
    """docstring for GridWidget"""

    def __init__(self, parent):
        super(GridWidget, self).__init__(parent)
        self.parent = parent
        self.init_ui()

        self.absMinValue = 1e-20
        self.absMaxValue = 1e20

        self.show()

    def init_ui(self):
        """ Docstring """

        imshowOpts = {'origin':'lower',
                      'cmap':'jet',
                      'interpolation':'bilinear'}

        self.obsCanvas = Canvas(parent=self, width=10, height=4, dpi=100)
        obsToolbar = NavigationToolbar(self.obsCanvas, self, coordinates=False)
        self.obs_im = self.obsCanvas.axes.imshow([[0.]], **imshowOpts)
        self.selCrossXobs, = self.obsCanvas.axes.plot([], [], '--', c='r', lw=0.5, zorder=0)
        self.selCrossYobs, = self.obsCanvas.axes.plot([], [], '--', c='r', lw=0.5, zorder=0)
        self.obsCanvas.fig.colorbar(self.obs_im)
        self.obsCanvas.canvasClicked.connect(self.canvasClicked)

        self.predCanvas = Canvas(parent=self, width=10, height=4, dpi=100)
        predToolbar = NavigationToolbar(self.predCanvas, self, coordinates=False)
        self.pred_im = self.predCanvas.axes.imshow([[0.]], **imshowOpts)
        self.selCrossXpred, = self.predCanvas.axes.plot([], [], '--', c='r', lw=0.5, zorder=0)
        self.selCrossYpred, = self.predCanvas.axes.plot([], [], '--', c='r', lw=0.5, zorder=0)
        self.predCanvas.fig.colorbar(self.pred_im)
        self.predCanvas.canvasClicked.connect(self.canvasClicked)

        self.highSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.highSlider.setMaximum(100)
        self.highSlider.setValue(100)
        self.highSlider.valueChanged.connect(self.setClim)

        self.lowSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.lowSlider.setMaximum(100)
        self.lowSlider.setValue(0)
        self.lowSlider.valueChanged.connect(self.setClim)

        lc1 = QtWidgets.QVBoxLayout()
        lc1.addWidget(self.obsCanvas)
        lc1.addWidget(obsToolbar)

        lc2 = QtWidgets.QVBoxLayout()
        lc2.addWidget(self.predCanvas)
        lc2.addWidget(predToolbar)

        lh = QtWidgets.QHBoxLayout()
        lh.addLayout(lc1)
        lh.addLayout(lc2)

        l = QtWidgets.QVBoxLayout(self)
        l.addLayout(lh)
        l.addWidget(self.highSlider)
        l.addWidget(self.lowSlider)

    def draw(self):
        self.obsCanvas.draw()
        self.predCanvas.draw()

    @QtCore.pyqtSlot(dict)
    def canvasClicked(self, event):
        signal = {'name':'closestLoc',
                  'x':event['xdata'],
                  'y':event['ydata']}
        self.ChangeSelectionSignal.emit(signal)

    def setClim(self):
        lsVal = self.lowSlider.value()
        hsVal = self.highSlider.value()
        if lsVal>=hsVal:
            self.lowSlider.setValue(hsVal-1)
            lsVal = self.lowSlider.value()
        dv = self.absMaxValue-self.absMinValue
        clMin = self.absMinValue+dv*lsVal/100.
        clMax = self.absMinValue+dv*hsVal/100.
        self.obs_im.set_clim(clMin, clMax)
        self.pred_im.set_clim(clMin, clMax)
        self.draw()

    def setLocation(self, loc):
        """ Docstring """
        x = loc.iloc[0].x
        y = loc.iloc[0].y
        self.selCrossXobs.set_data(self.obsCanvas.axes.get_xlim(),[y,y])
        self.selCrossYobs.set_data([x,x],self.obsCanvas.axes.get_ylim())
        self.selCrossXpred.set_data(self.predCanvas.axes.get_xlim(),[y,y])
        self.selCrossYpred.set_data([x,x],self.predCanvas.axes.get_ylim())
        self.draw()

    def setTime(self, data_times):

        tInd = data_times.iloc[0].tInd

        if 'dBdt_Z' in self.parent.gridStore:
            grid_obs = self.parent.gridStore['dBdt_Z'][tInd]['grid']
            x_vector = self.parent.gridStore['dBdt_Z'][tInd]['x_vector']
            y_vector = self.parent.gridStore['dBdt_Z'][tInd]['y_vector']

            self.obs_im.set_data(grid_obs)
            self.obs_im.set_extent((x_vector[0], x_vector[-1],
                                    y_vector[0], y_vector[-1]))

            self.absMinValue = np.nanmin(grid_obs)
            self.absMaxValue = np.nanmax(grid_obs)

        if 'dBdt_Z_pred' in self.parent.gridStore:
            grid_pred = self.parent.gridStore['dBdt_Z_pred'][tInd]['grid']
            x_vector = self.parent.gridStore['dBdt_Z_pred'][tInd]['x_vector']
            y_vector = self.parent.gridStore['dBdt_Z_pred'][tInd]['y_vector']

            if np.any(grid_pred):
                self.pred_im.set_data(grid_pred)
                self.pred_im.set_extent((x_vector[0], x_vector[-1],
                                         y_vector[0], y_vector[-1]))
            else:
                self.pred_im.set_data(np.nan*np.ones((2, 2)))

        self.setClim()
        self.draw()

