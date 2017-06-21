
import numpy as np
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
from .ATEMWidget import ATEMWidget

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

class LineWidget(ATEMWidget):
    """docstring for LineWidget"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.show()

    def init_ui(self):
        """ Docstring """

        # Make the background white
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(palette)

        self.titleLabel = QtWidgets.QLabel()
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setLogMode(x=False, y=True)
        self.plotWidget.setLabel('left', 'dB/dt')
        # self.plotWidget.setLabel('bottom', 'Time', units='s')

        linePen = {'color': 'k', 'width': 2}
        self.datLines = {}
        for i, t in self.parent.data.times.iterrows():
            self.datLines[i] = pg.PlotDataItem(pen=linePen)

        # Crosshair
        self.chvLine = pg.InfiniteLine(angle=90, movable=False, pen={'color':'k', 'width':0.25})
        self.chhLine = pg.InfiniteLine(angle=0, movable=False, pen={'color':'k', 'width':0.25})

        self.plotWidget.addItem(self.chvLine, ignoreBounds=True)
        self.plotWidget.addItem(self.chhLine, ignoreBounds=True)
        for line in self.datLines.values():
            self.plotWidget.addItem(line)

        # uncertBounds.setZValue(0)
        # self.selectedLocLine.setZValue(1)
        # self.obsPlot.setZValue(2)
        # self.predPlot.setZValue(3)
        # self.chvLine.setZValue(4)
        # self.chhLine.setZValue(5)
        # legend.setZValue(6)
        #
        l = QtWidgets.QVBoxLayout(self)
        l.addWidget(self.titleLabel)
        l.addWidget(self.plotWidget)
        #
        self.mouseMoveProxy = pg.SignalProxy(self.plotWidget.scene().sigMouseMoved,
                                             rateLimit=30,
                                             slot=self.mouseMovedEvent)
        self.plotWidget.scene().sigMouseClicked.connect(self.clickEvent)

    def mouseMovedEvent(self, pos):
        pos = pos[0]
        if self.plotWidget.sceneBoundingRect().contains(pos):
            mousePoint = self.plotWidget.getViewBox().mapSceneToView(pos)
            self.chvLine.setPos(mousePoint.x())
            self.chhLine.setPos(mousePoint.y())
    #
    def clickEvent(self, event):
        if self.plotWidget.sceneBoundingRect().contains(event.scenePos()):
            mousePoint = self.plotWidget.getViewBox().mapSceneToView(event.scenePos())
            print(mousePoint)
    #         signal = {'name':'closestTime',
    #                   't':10**mousePoint.x()}
    #         self.ChangeSelectionSignal.emit(signal)
        else:
            pass

    def setLocation(self, loc):
        """ Docstring """
        lineN = loc.iloc[0].line
        line = self.parent.data.getLine(lineN)
        for i in self.parent.data.times.index:
            td = line[line.tInd == i]
            self.datLines[i].setData(td.x.values, td.dBdt_Z.values)
        self.plotWidget.setXRange(line.x.min(), line.x.max())
        self.plotWidget.setYRange(np.log10(line.dBdt_Z.min()), np.log10(line.dBdt_Z.max()))
        self.titleLabel.setText('{}'.format(lineN))

    #     t = loc.t.values
    #     obs = loc.dBdt_Z.values
    #     self.obsPlot.setData(t, obs)
    #
    #     if loc.dBdt_Z_pred.any():
    #         pred = loc.dBdt_Z_pred.values
    #         self.predPlot.setData(t, pred)
    #
    #     if loc.dBdt_Z_uncert.any():
    #         lower = obs - loc.dBdt_Z_uncert.values
    #         upper = obs + loc.dBdt_Z_uncert.values
    #         lower[lower < 0.] = obs.min()/100.
    #         self.upperPlot.setData(t, lower)
    #         self.lowerPlot.setData(t, upper)

    def setTime(self, time):
        """ docstring """
        pass
    #     self.selectedLocLine.setPos(np.log10(time.values))
