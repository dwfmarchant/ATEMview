""" ATEMview Location Window """
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
from .ATEMWidget import ATEMWidget
from .colormaps import jetCM, jetBrush

class LocWidget(ATEMWidget):
    """docstring for LocWidget"""

    def __init__(self, parent):
        super(LocWidget, self).__init__(parent)
        self.parent = parent
        self.init_ui()
        self.showData = False
        self.data = None
        self.x = None
        self.y = None
        self.minVal = 1.
        self.maxVal = 1.
        self.show()

    def init_ui(self):
        """ Docstring """

        # Make the background white
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(palette)

        self.plotWidget = pg.PlotWidget(enableMenu=False)
        self.plotWidget.setLabel('left', 'Easting', units='m')
        self.plotWidget.setLabel('bottom', 'Northing', units='m')
        self.plotWidget.showGrid(x=True, y=True)
        self.plotWidget.getViewBox().setAspectLocked()

        self.scatter = pg.ScatterPlotItem(pen=None, pxMode=True)
        self.plotWidget.addItem(self.scatter)

        self.selectedLocVline = pg.InfiniteLine(angle=90,
                                                movable=False,
                                                pen={'color':'k',
                                                     'width':2,
                                                     'style':QtCore.Qt.DotLine})
        self.plotWidget.addItem(self.selectedLocVline, ignoreBounds=True)

        self.selectedLocHline = pg.InfiniteLine(angle=0,
                                                movable=False,
                                                pen={'color':'k',
                                                     'width':2,
                                                     'style':QtCore.Qt.DotLine})
        self.plotWidget.addItem(self.selectedLocHline, ignoreBounds=True)

        self.plotWidget.scene().sigMouseClicked.connect(self.clickEvent)

        self.colorbarWidget = pg.PlotWidget(enableMenu=False)
        self.colorbarWidget.setMaximumWidth(100)
        self.colorbarWidget.getViewBox().setMouseEnabled(False, False)
        self.colorbarWidget.setXRange(0, 20, padding=0)
        self.colorbarWidget.setYRange(0, 256, padding=0)
        self.colorbarWidget.getAxis('bottom').setPen(None)
        self.colorbarWidget.getAxis('left').setPen(None)
        self.colorbarWidget.setVisible(False)

        self.cbMinLabel = QtWidgets.QLabel()
        self.cbMinLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.cbMinLabel.setText('0.00')
        self.cbMaxLabel = QtWidgets.QLabel()
        self.cbMaxLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.cbMaxLabel.setText('1.00')

        self.colorbar = pg.ImageItem()
        cbData = np.arange(0, 256)[:, np.newaxis].repeat(20, axis=1).T
        self.colorbar.setImage(jetCM[cbData])

        self.colorbarWidget.addItem(self.colorbar)

        self.misfitCheckBox = QtWidgets.QCheckBox('Show Misfit')
        self.misfitCheckBox.toggled.connect(self.toggleMisfit)

        self.maxCvalSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.maxCvalSlider.setMaximum(100)
        self.maxCvalSlider.setValue(100)
        self.maxCvalSlider.valueChanged.connect(self.setClim)
        self.maxCvalSlider.setVisible(False)

        cbvLayout = QtWidgets.QVBoxLayout()
        cbvLayout.addWidget(self.cbMaxLabel)
        cbvLayout.addWidget(self.colorbarWidget)
        cbvLayout.addWidget(self.cbMinLabel)

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.plotWidget)
        hLayout.addLayout(cbvLayout)

        vLayout = QtWidgets.QVBoxLayout(self)
        vLayout.addWidget(self.misfitCheckBox)
        vLayout.addLayout(hLayout)

        vLayout.addWidget(self.maxCvalSlider)


    def clickEvent(self, event):
        if self.plotWidget.sceneBoundingRect().contains(event.scenePos()):
            mousePoint = self.plotWidget.getViewBox().mapSceneToView(event.scenePos())
            signal = {'name':'closestLoc',
                      'x':mousePoint.x(),
                      'y':mousePoint.y()}
            self.ChangeSelectionSignal.emit(signal)
        else:
            pass

    @QtCore.pyqtSlot(bool)
    def toggleMisfit(self, show):
        """ Callback that gets fired 'Show Misfit' box is toggled """
        if show:
            self.colorbarWidget.setVisible(True)
            self.maxCvalSlider.setVisible(True)
            self.showData = True
        else:
            self.colorbarWidget.setVisible(False)
            self.maxCvalSlider.setVisible(False)
            self.showData = False
        self.updatePlot()

    def updatePlot(self):
        if self.showData:
            hsVal = self.maxCvalSlider.value()
            maxVal = self.maxVal*hsVal/100.
            self.cbMaxLabel.setText('{:.2f}'.format(maxVal))
            bins = np.linspace(0., maxVal, 255)
            di = np.digitize(self.data, bins)-1
            self.scatter.setData(self.x, self.y,
                                 pen=None,
                                 brush=jetBrush[di],
                                 symbolSize=10.)
        else:
            self.scatter.setData(self.x, self.y, pen=None, brush='k', symbolSize=10.)

    def setAll(self, x, y):
        """ Docstring """
        self.scatter.setData(x, y, pen=None, brush='k', symbolSize=10.)
        self.plotWidget.setXRange(x.min()-100., x.max()+100.)
        self.plotWidget.setYRange(y.min()-100., y.max()+100.)

    def setLocation(self, loc):
        """ Docstring """
        xl = loc.iloc[0].x
        yl = loc.iloc[0].y
        self.selectedLocVline.setPos(xl)
        self.selectedLocHline.setPos(yl)

    def setTime(self, data_times):
        """ Set the displayed misfit data """
        self.x = data_times.x.values
        self.y = data_times.y.values
        self.data = (data_times.dBdt_Z-data_times.dBdt_Z_pred).abs()/data_times.dBdt_Z_uncert
        self.minVal = self.data.min()
        self.maxVal = self.data.max()
        self.updatePlot()

    def setClim(self):
        """ Set the color limits on the misfit scatter plot """
        self.updatePlot()
