
from PyQt5 import QtCore, QtWidgets
import numpy as np
import pyqtgraph as pg
from .ATEMWidget import ATEMWidget
from .GridWorker import GridWorker
from .colormaps import jetCM

class GridWidget(ATEMWidget):
    """docstring for GridWidget"""

    def __init__(self, parent, component):
        super(GridWidget, self).__init__(parent)
        self.parent = parent
        self.ach = 'dBdt_' + self.parent.selectedComponent
        self.isMoment = self.parent.isMoment
        self.selectedMoment = self.parent.selectedMoment if self.isMoment else 'N'
        self.gridStore = {'N': {}, 'L': {}, 'H': {}}
        # self.init_grids()
        self.init_ui()
        if not self.parent.data.has_pred:
            self.predPlotWidget.setVisible(False)

        self.absMinValue = 1e-20
        self.absMaxValue = 1e20

        self.show()

    def init_ui(self):
        """ Docstring """

        # Make the background white
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(palette)

        self.obsPlotWidget = pg.PlotWidget(enableMenu=False)
        self.obsPlotWidget.setLabel('left', 'Easting', units='m')
        self.obsPlotWidget.setLabel('bottom', 'Northing', units='m')
        self.obsPlotWidget.showGrid(x=True, y=True)
        self.obsPlotWidget.getViewBox().setAspectLocked()
        self.obsPlotWidget.setTitle('Observed')

        self.predPlotWidget = pg.PlotWidget(enableMenu=False)
        self.predPlotWidget.setLabel('left', 'Easting', units='m')
        self.predPlotWidget.setLabel('bottom', 'Northing', units='m')
        self.predPlotWidget.showGrid(x=True, y=True)
        self.predPlotWidget.getViewBox().setAspectLocked()
        self.predPlotWidget.setTitle('Predicted')

        self.colorbarWidget = pg.PlotWidget(enableMenu=False)
        self.colorbarWidget.setMaximumWidth(40)
        self.colorbarWidget.getViewBox().setMouseEnabled(False, False)
        self.colorbarWidget.setXRange(0, 20, padding=0)
        self.colorbarWidget.setYRange(0, 256, padding=0)
        self.colorbarWidget.getAxis('bottom').setPen(None)
        self.colorbarWidget.getAxis('left').setPen(None)
        self.colorbarWidget.getAxis('left').setWidth(0)
        self.colorbarWidget.getAxis('right').setWidth(0)
        self.colorbarWidget.getAxis('top').setWidth(0)
        self.colorbarWidget.getAxis('bottom').setWidth(0)

        self.cbMinLabel = QtWidgets.QLabel()
        self.cbMinLabel.setText('')
        self.cbMaxLabel = QtWidgets.QLabel()
        self.cbMaxLabel.setText('')

        self.colorbar = pg.ImageItem()
        cbData = np.arange(0, 256)[:, np.newaxis].repeat(20, axis=1).T
        self.colorbar.setImage(jetCM[cbData])
        self.colorbarWidget.addItem(self.colorbar)

        self.locLabel = QtWidgets.QLabel('')
        self.locLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.obsImage = pg.ImageItem()
        self.obsPlotWidget.addItem(self.obsImage)

        self.predImage = pg.ImageItem()
        self.predPlotWidget.addItem(self.predImage)

        locLinePen = {'color':'k', 'width':2, 'style':QtCore.Qt.DotLine}
        self.selectedLocVlineObs = pg.InfiniteLine(angle=90, movable=False, pen=locLinePen)
        self.selectedLocVlinePred = pg.InfiniteLine(angle=90, movable=False, pen=locLinePen)
        self.obsPlotWidget.addItem(self.selectedLocVlineObs, ignoreBounds=True)
        self.predPlotWidget.addItem(self.selectedLocVlinePred, ignoreBounds=True)
        self.selectedLocHlineObs = pg.InfiniteLine(angle=0, movable=False, pen=locLinePen)
        self.selectedLocHlinePred = pg.InfiniteLine(angle=0, movable=False, pen=locLinePen)
        self.obsPlotWidget.addItem(self.selectedLocHlineObs, ignoreBounds=True)
        self.predPlotWidget.addItem(self.selectedLocHlinePred, ignoreBounds=True)

        self.obsPlotWidget.scene().sigMouseClicked.connect(self.clickObsEvent)
        self.predPlotWidget.scene().sigMouseClicked.connect(self.clickPredEvent)
        self.obsPlotWidget.setXLink(self.predPlotWidget)
        self.obsPlotWidget.setYLink(self.predPlotWidget)

        self.highSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.highSlider.setMaximum(100)
        self.highSlider.setValue(100)
        self.highSlider.valueChanged.connect(self.setClim)

        self.lowSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.lowSlider.setMaximum(100)
        self.lowSlider.setValue(0)
        self.lowSlider.valueChanged.connect(self.setClim)

        lh = QtWidgets.QHBoxLayout()
        lh.addWidget(self.obsPlotWidget)
        lh.addWidget(self.predPlotWidget)

        cbvLayout = QtWidgets.QVBoxLayout()
        cbvLayout.addWidget(self.cbMaxLabel)
        cbvLayout.addWidget(self.colorbarWidget)
        cbvLayout.addWidget(self.cbMinLabel)
        lh.addLayout(cbvLayout)

        l = QtWidgets.QVBoxLayout(self)
        l.addLayout(lh)
        l.addWidget(self.highSlider)
        l.addWidget(self.lowSlider)
        l.addWidget(self.locLabel)

        self.mouseMoveProxyObs = pg.SignalProxy(self.obsPlotWidget.scene().sigMouseMoved,
                                                rateLimit=30, slot=self.mouseMovedEvent)
        self.mouseMoveProxyPred = pg.SignalProxy(self.predPlotWidget.scene().sigMouseMoved,
                                                 rateLimit=30, slot=self.mouseMovedEvent)

    def init_grids(self):

        if self.isMoment:
            self.gridWorker_LObs = GridWorker(self.parent.data, self.ach, 'L')
            self.gridWorker_HObs = GridWorker(self.parent.data, self.ach, 'H')
        else:
            self.gridWorker_Obs = GridWorker(self.parent.data, self.ach)

        gws = [self.gridWorker_LObs, self.gridWorker_HObs] if self.isMoment else [self.gridWorker_Obs]

        for gw in gws:
            gw.finishedGrid.connect(self.storeGrid)
            gw.grdOpts['number_cells'] = 256
            gw.start()

        if self.parent.data.has_pred:
            if self.isMoment:
                self.gridWorker_LPred = GridWorker(self.parent.data, self.ach + '_pred', 'L')
                self.gridWorker_HPred = GridWorker(self.parent.data, self.ach + '_pred', 'H')
            else:
                self.gridWorker_Pred = GridWorker(self.parent.data, self.ach + '_pred')

            gws = [self.gridWorker_LPred, self.gridWorker_HPred] if self.isMoment else [self.gridWorker_Pred]

            for gw in gws:
                gw.finishedGrid.connect(self.storeGrid)
                gw.grdOpts['number_cells'] = 256
                gw.start()

    @QtCore.pyqtSlot(dict)
    def storeGrid(self, event):
        if event['ch'] not in self.gridStore[event['moment']]:
            self.gridStore[event['moment']][event['ch']] = {}
        self.gridStore[event['moment']][event['ch']][event['tInd']] = event

        if event['tInd'] == self.selectedTimeInd:
            if event['ch'] == self.ach:
                if event['moment'] == self.selectedMoment:
                    self.absMinValue = np.nanmin(event['grid'])
                    self.absMaxValue = np.nanmax(event['grid'])
                    self.drawObs()
                    try:
                        self.drawPred()
                    except Exception as e:
                        pass
                    self.obsPlotWidget.autoRange()
            if event['ch'] == self.ach + '_pred':
                if event['moment'] == self.selectedMoment:
                    self.drawPred()
                    try:
                        self.drawObs()
                    except Exception as e:
                        pass
                    self.predPlotWidget.autoRange()

    def clickObsEvent(self, event):
        if self.obsPlotWidget.sceneBoundingRect().contains(event.scenePos()):
            mousePoint = self.obsPlotWidget.getViewBox().mapSceneToView(event.scenePos())
            signal = {'name':'closestLoc',
                      'x':mousePoint.x(),
                      'y':mousePoint.y()}
            self.ChangeSelectionSignal.emit(signal)
        else:
            pass

    def clickPredEvent(self, event):
        if self.predPlotWidget.sceneBoundingRect().contains(event.scenePos()):
            mousePoint = self.predPlotWidget.getViewBox().mapSceneToView(event.scenePos())
            signal = {'name':'closestLoc',
                      'x':mousePoint.x(),
                      'y':mousePoint.y()}
            self.ChangeSelectionSignal.emit(signal)
        else:
            pass

    def mouseMovedEvent(self, pos):
        pos = pos[0]
        if self.obsPlotWidget.sceneBoundingRect().contains(pos):
            mousePoint = self.obsPlotWidget.getViewBox().mapSceneToView(pos)
            string = "<span style='font-size: 12pt'>x={:.0f}, y={:.0f}</span>"
            self.locLabel.setText(string.format(mousePoint.x(), mousePoint.y()))
        elif self.predPlotWidget.sceneBoundingRect().contains(pos):
            mousePoint = self.predPlotWidget.getViewBox().mapSceneToView(pos)
            string = "<span style='font-size: 12pt'>x={:.0f}, y={:.0f}</span>"
            self.locLabel.setText(string.format(
                mousePoint.x(), mousePoint.y()))["moment"]

            # self.chvLine.setPos(mousePoint.x())
            # self.chhLine.setPos(mousePoint.y())

    def setClim(self):

        lsVal = self.lowSlider.value()
        hsVal = self.highSlider.value()
        if lsVal >= hsVal:
            self.lowSlider.setValue(hsVal-1)
            lsVal = self.lowSlider.value()
        self.drawObs()
        if self.ach +'_pred' in self.gridStore[self.selectedMoment]:
            self.drawPred()

    def getClim(self):
        lsVal = self.lowSlider.value()
        hsVal = self.highSlider.value()
        dv = self.absMaxValue-self.absMinValue
        clMin = self.absMinValue+dv*lsVal/100.
        clMax = self.absMinValue+dv*hsVal/100.
        return clMin, clMax

    def setLocation(self, loc):
        """ Docstring """
        xl = loc.iloc[0].x
        yl = loc.iloc[0].y
        self.selectedLocVlineObs.setPos(xl)
        self.selectedLocHlineObs.setPos(yl)
        self.selectedLocVlinePred.setPos(xl)
        self.selectedLocHlinePred.setPos(yl)

    def setTime(self, data_times):
        self.selectedTimeInd = data_times.iloc[0].tInd
        if self.ach in self.gridStore[self.selectedMoment]:
            grid_obs = self.gridStore[self.selectedMoment][self.ach][self.selectedTimeInd]['grid']
            self.absMinValue = np.nanmin(grid_obs)
            self.absMaxValue = np.nanmax(grid_obs)
            self.drawObs()
        if self.ach + '_pred' in self.gridStore[self.selectedMoment]:
            self.drawPred()

    def setComponent(self, component):
        self.ach = 'dBdt_' + component

    def setMoment(self, moment):
        self.isMoment = True
        self.selectedMoment = moment
        # self.selectedTimeInd = 0
        # if self.ach in self.gridStore[self.selectedMoment]:
        #     grid_obs = self.gridStore[self.selectedMoment][self.ach][self.selectedTimeInd]['grid']
        #     self.absMinValue = np.nanmin(grid_obs)
        #     self.absMaxValue = np.nanmax(grid_obs)
        #     self.drawObs()
        # if self.ach + '_pred' in self.gridStore[self.selectedMoment]:
        #     self.drawPred()

    def drawObs(self):

        grid_obs = self.gridStore[self.selectedMoment][self.ach][self.selectedTimeInd]['grid'].T
        x_vector = self.gridStore[self.selectedMoment][self.ach][self.selectedTimeInd]['x_vector']
        y_vector = self.gridStore[self.selectedMoment][self.ach][self.selectedTimeInd]['y_vector']
        clMin, clMax = self.getClim()
        bins = np.linspace(clMin, clMax, 255)
        cInd_obs = np.digitize(grid_obs, bins)
        colors_obs = jetCM[cInd_obs]
        colors_obs[np.isnan(grid_obs)] = (0, 0, 0, 0)
        self.obsImage.setImage(colors_obs)
        self.obsImage.setPos(x_vector.min(), y_vector.min())
        self.obsImage.setScale(x_vector[1]-x_vector[0])
        self.cbMaxLabel.setText('{:.2e}'.format(clMax))
        self.cbMinLabel.setText('{:.2e}'.format(clMin))

    def drawPred(self):

        grid_pred = self.gridStore[self.selectedMoment][self.ach + '_pred'][self.selectedTimeInd]['grid'].T
        x_vector = self.gridStore[self.selectedMoment][self.ach + '_pred'][self.selectedTimeInd]['x_vector']
        y_vector = self.gridStore[self.selectedMoment][self.ach + '_pred'][self.selectedTimeInd]['y_vector']

        if np.any(grid_pred):
            clMin, clMax = self.getClim()
            bins = np.linspace(clMin, clMax, 255)
            cInd_pred = np.digitize(grid_pred, bins)
            colors_pred = jetCM[cInd_pred]
            colors_pred[np.isnan(grid_pred)] = (0, 0, 0, 0)
            self.predImage.setImage(colors_pred)
            self.predImage.setPos(x_vector.min(), y_vector.min())
            self.predImage.setScale(x_vector[1]-x_vector[0])
        else:
            self.predImage.setImage(None)
