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
        # self.ach = 'dBdt_' + parent.active_component
        self.init_ui()
        self.showData = False
        self.data = None
        self.tInd = -1
        self.x = None
        self.y = None
        self.minVal = 1.
        self.maxVal = 1.
        self.cbFormatStr = '{:.2f}'
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

        self.selectCombo = QtWidgets.QComboBox()
        self.selectCombo.addItem("Misfit (time)")
        self.selectCombo.addItem("Misfit (total)")
        self.selectCombo.addItem("Observed")
        self.selectCombo.addItem("Predicted")
        self.selectCombo.activated[str].connect(self.changeCombo)
        self.selectCombo.setVisible(False)

        self.titleLabel = QtWidgets.QLabel(self.selectCombo.currentText())
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.titleLabel.setVisible(False)

        self.maxCvalSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.maxCvalSlider.setMaximum(100)
        self.maxCvalSlider.setValue(100)
        self.maxCvalSlider.valueChanged.connect(self.setClim)
        self.maxCvalSlider.setVisible(False)

        self.minCvalSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.minCvalSlider.setMaximum(100)
        self.minCvalSlider.setValue(0)
        self.minCvalSlider.valueChanged.connect(self.updatePlot)
        self.minCvalSlider.setVisible(False)

        cbvLayout = QtWidgets.QVBoxLayout()
        cbvLayout.addWidget(self.cbMaxLabel)
        cbvLayout.addWidget(self.colorbarWidget)
        cbvLayout.addWidget(self.cbMinLabel)

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.plotWidget)
        hLayout.addLayout(cbvLayout)

        vLayout = QtWidgets.QVBoxLayout(self)

        hMisLayout = QtWidgets.QHBoxLayout()
        hMisLayout.addWidget(self.misfitCheckBox)
        hMisLayout.addWidget(self.selectCombo)

        vLayout.addLayout(hMisLayout)
        vLayout.addWidget(self.titleLabel)
        vLayout.addLayout(hLayout)

        vLayout.addWidget(self.maxCvalSlider)
        vLayout.addWidget(self.minCvalSlider)

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
        if self.data is not None:
            if show:
                self.colorbarWidget.setVisible(True)
                self.maxCvalSlider.setVisible(True)
                self.minCvalSlider.setVisible(True)
                self.selectCombo.setVisible(True)
                self.titleLabel.setVisible(True)
                self.showData = True
            else:
                self.colorbarWidget.setVisible(False)
                self.maxCvalSlider.setVisible(False)
                self.minCvalSlider.setVisible(False)
                self.selectCombo.setVisible(False)
                self.titleLabel.setVisible(False)
            self.updatePlot()

    @QtCore.pyqtSlot(str)
    def changeCombo(self, text):
        if self.selectCombo.currentText() == "Misfit (time)":
            self.cbFormatStr = "{:.2f}"
        elif self.selectCombo.currentText() == "Misfit (total)":
            self.cbFormatStr = "{:.2f}"
        elif self.selectCombo.currentText() == "Observed":
            self.cbFormatStr = "{:.2e}"
        elif self.selectCombo.currentText() == "Predicted":
            self.cbFormatStr = "{:.2e}"
        self.titleLabel.setText(text)
        self.setData()
        self.updatePlot()

    def updatePlot(self):
        if self.showData & (self.data is not None):
            clMin, clMax = self.getClim()
            self.cbMaxLabel.setText(self.cbFormatStr.format(clMax))
            self.cbMinLabel.setText(self.cbFormatStr.format(clMin))
            bins = np.linspace(clMin, clMax, 255)
            di = np.digitize(self.data, bins)
            self.scatter.setData(self.x, self.y, pen=None,
                                 brush=jetBrush[di], symbolSize=10.)
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
        self.tInd = data_times.tInd.iloc[0]
        if self.selectCombo.currentText() != "Misfit (total)":
            self.setData()
        self.updatePlot()

    def setComponent(self, component):
        self.ach = 'dBdt_' + component

    def setData(self):
        data_time = self.parent.data.getTime(self.tInd)
        self.x = data_time.x.values
        self.y = data_time.y.values
        if self.selectCombo.currentText() == "Misfit (time)":
            if data_time[self.ach + '_pred'].any():
                self.data = (data_time[self.ach]-data_time[self.ach + '_pred']).abs()/data_time[self.ach + '_uncert']
            else:
                self.data = None
        elif self.selectCombo.currentText() == "Misfit (total)":
            if data_time[self.ach + '_pred'].any():
                grp = self.parent.data.df.groupby('locInd')
                l22 = lambda g: np.linalg.norm((g[self.ach] - g[self.ach + '_pred'])/g[self.ach + '_uncert'])**2/g.shape[0]
                grp = grp.agg(l22)[['x', 'y', self.ach]]
                self.data = grp[self.ach].values
                self.x = self.parent.data.locs.sort_index().x.values
                self.y = self.parent.data.locs.sort_index().y.values
                # print(self.data)
            else:
                self.data = None
        elif self.selectCombo.currentText() == "Observed":
            self.data = data_time[self.ach]
        elif self.selectCombo.currentText() == "Predicted":
            self.data = data_time[self.ach + '_pred']
        else:
            self.data = None
        if self.data is not None:
            self.minVal = self.data.min()
            self.maxVal = self.data.max()

    def setClim(self):
        """ Set the color limits on the misfit scatter plot """
        lsVal = self.minCvalSlider.value()
        hsVal = self.maxCvalSlider.value()
        if lsVal >= hsVal:
            self.minCvalSlider.setValue(hsVal-1)
            lsVal = self.minCvalSlider.value()
        self.updatePlot()

    def getClim(self):
        lsVal = self.minCvalSlider.value()
        hsVal = self.maxCvalSlider.value()
        dv = self.data.max()-self.data.min()
        clMin = self.data.min()+dv*lsVal/100.
        clMax = self.data.min()+dv*hsVal/100.
        return clMin, clMax
