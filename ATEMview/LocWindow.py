""" ATEMview Location Window """
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from .Canvas import Canvas
from .ATEMWidget import ATEMWidget

class LocWidget(ATEMWidget):
    """docstring for LocWidget"""

    def __init__(self, parent):
        super(LocWidget, self).__init__(parent)
        self.parent = parent
        self.init_ui()
        self.init_plot()
        self.show()

    def init_ui(self):
        """ Docstring """
        self.canvas = Canvas(parent=self, width=5, height=4, dpi=100)
        self.canvas.canvasClicked.connect(self.canvasClicked)

        self.misfitCheckBox = QtWidgets.QCheckBox('Show Misfit')
        self.misfitCheckBox.toggled.connect(self.toggleMisfit)

        self.maxCvalSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.maxCvalSlider.setMaximum(100)
        self.maxCvalSlider.setValue(100)
        self.maxCvalSlider.valueChanged.connect(self.setClim)

        toolbar = NavigationToolbar(self.canvas, self, coordinates=False)
        vLayout = QtWidgets.QVBoxLayout(self)
        vLayout.addWidget(self.misfitCheckBox)
        vLayout.addWidget(self.canvas)
        vLayout.addWidget(toolbar)
        vLayout.addWidget(self.maxCvalSlider)

    def init_plot(self):
        """ Initialize the plot """
        self.selCrossX, = self.canvas.axes.plot([], [], '--', c='r', lw=0.5, zorder=0)
        self.selCrossY, = self.canvas.axes.plot([], [], '--', c='r', lw=0.5, zorder=1)
        self.allPlot, = self.canvas.axes.plot([], [], 'o', c='k', ms=1., zorder=2)
        self.selPlot, = self.canvas.axes.plot([], [], 'o', c='r', ms=2., zorder=3)
        self.scatter = self.canvas.axes.scatter([], [], c=[], s=5, cmap='jet',
                                                zorder=4, visible=False)
        self.cbar = self.canvas.fig.colorbar(self.scatter, pad=0., aspect=40)
        self.cbar.ax.set_visible(False)
        self.canvas.axes.set_aspect('equal')

    @QtCore.pyqtSlot(dict)
    def canvasClicked(self, event):
        """ Callback that gets fired when the plot axis is clicked """
        signal = {'name':'closestLoc',
                  'x':event['xdata'],
                  'y':event['ydata']}
        self.ChangeSelectionSignal.emit(signal)

    @QtCore.pyqtSlot(bool)
    def toggleMisfit(self, show):
        """ Callback that gets fired 'Show Misfit' box is toggled """
        if show:
            if not self.scatter.get_array().any():
                signal = {'name':'sameTime'}
                self.ChangeSelectionSignal.emit(signal)
            self.scatter.set_visible(True)
            self.cbar.ax.set_visible(True)
        else:
            self.scatter.set_visible(False)
            self.cbar.ax.set_visible(False)
        self.canvas.draw()

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
        self.selCrossX.set_data(self.canvas.axes.get_xlim(), [y, y])
        self.selCrossY.set_data([x, x], self.canvas.axes.get_ylim())
        self.canvas.draw()

    def setTime(self, data_times):
        """ Set the displayed misfit data """
        misfit = (data_times.dBdt_Z-data_times.dBdt_Z_pred).abs()/data_times.dBdt_Z_uncert
        self.scatter.set_offsets(data_times[['x', 'y']])
        self.scatter.set_array(misfit)
        self.setClim()

    def setClim(self):
        """ Set the color limits on the misfit scatter plot """
        hsVal = self.maxCvalSlider.value()
        misfitRange = self.scatter.get_array().max() - self.scatter.get_array().min()
        clMax = self.scatter.get_array().min()+misfitRange*hsVal/100.
        self.scatter.set_clim(0., clMax)
        self.canvas.draw()
