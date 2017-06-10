
import numpy as np
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
from .ATEMWidget import ATEMWidget

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

class DecayWidget(ATEMWidget):
    """docstring for LocWidget"""
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
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)


        self.win = pg.GraphicsWindow()
        # self.win = pg.GraphicsWidget()
        self.chLabel = pg.LabelItem(justify='right')
        self.win.addItem(self.chLabel)

        self.plotWidget = self.win.addPlot(row=1, col=0)
        self.plotWidget.setLogMode(x=True, y=True)
        self.plotWidget.setLabel('left', 'dB/dt')
        self.plotWidget.setLabel('bottom', 'Time', units='s')
        legend = self.plotWidget.addLegend(offset=(450, 30))
        self.plotWidget.showGrid(x=True, y=True)

        self.obsPlot = pg.PlotDataItem(symbol='o',
                                       symbolSize=5,
                                       symbolBrush='k',
                                       pen={'color': 'k',
                                            'width': 2},
                                       name='Obs.')

        self.predPlot = pg.PlotDataItem(symbol='o',
                                        symbolSize=5,
                                        symbolBrush='r',
                                        pen={'color': 'r',
                                             'width': 2},
                                        name='Pred.')

        self.selectedTimeLine = pg.InfiniteLine(angle=90,
                                                movable=False,
                                                pen={'color':'k',
                                                     'width':2,
                                                     'style':QtCore.Qt.DotLine})


        self.lowerPlot = pg.PlotDataItem()
        self.upperPlot = pg.PlotDataItem()
        uncertBounds = pg.FillBetweenItem(self.lowerPlot, self.upperPlot, 0.8)

        # Crosshair
        self.chvLine = pg.InfiniteLine(angle=90, movable=False, pen={'color':'k', 'width':0.25})
        self.chhLine = pg.InfiniteLine(angle=0, movable=False, pen={'color':'k', 'width':0.25})

        self.plotWidget.addItem(self.chvLine, ignoreBounds=True)
        self.plotWidget.addItem(self.chhLine, ignoreBounds=True)
        self.plotWidget.addItem(self.obsPlot)
        self.plotWidget.addItem(self.predPlot)
        self.plotWidget.addItem(self.selectedTimeLine, ignoreBounds=True)
        self.plotWidget.addItem(uncertBounds, ignoreBounds=True)
        self.plotWidget.addItem(self.lowerPlot, ignoreBounds=True)
        self.plotWidget.addItem(self.upperPlot, ignoreBounds=True)

        uncertBounds.setZValue(0)
        self.selectedTimeLine.setZValue(1)
        self.obsPlot.setZValue(2)
        self.predPlot.setZValue(3)
        self.chvLine.setZValue(4)
        self.chhLine.setZValue(5)
        legend.setZValue(6)

        l = QtWidgets.QVBoxLayout(self)
        l.addWidget(self.titleLabel)
        l.addWidget(self.win)

        self.mouseMoveProxy = pg.SignalProxy(self.plotWidget.scene().sigMouseMoved,
                                             rateLimit=30,
                                             slot=self.mouseMovedEvent)
        self.plotWidget.scene().sigMouseClicked.connect(self.clickEvent)

    def mouseMovedEvent(self, pos):
        pos = pos[0]
        if self.plotWidget.sceneBoundingRect().contains(pos):
            mousePoint = self.plotWidget.getViewBox().mapSceneToView(pos)
            string = "<span style='font-size: 12pt'>x={:.2e}, t={:.2e}</span>"
            self.chLabel.setText(string.format(10**mousePoint.x(), 10**mousePoint.y()))
            self.chvLine.setPos(mousePoint.x())
            self.chhLine.setPos(mousePoint.y())

    def clickEvent(self, event):
        if self.plotWidget.sceneBoundingRect().contains(event.scenePos()):
            mousePoint = self.plotWidget.getViewBox().mapSceneToView(event.scenePos())
        signal = {'name':'closestTime',
                  't':10**mousePoint.x()}
        self.ChangeSelectionSignal.emit(signal)

    def setLocation(self, loc):
        """ Docstring """
        t = loc.t.values
        obs = loc.dBdt_Z.values
        pred = loc.dBdt_Z_pred.values
        lower = obs - loc.dBdt_Z_uncert.values
        upper = obs + loc.dBdt_Z_uncert.values
        lower[lower < 0.] = obs.min()/10.

        self.obsPlot.setData(t, obs)
        self.predPlot.setData(t, pred)
        self.upperPlot.setData(t, lower)
        self.lowerPlot.setData(t, upper)

        self.plotWidget.setXRange(np.log10(t.min()), np.log10(t.max()))
        self.plotWidget.setYRange(np.log10(obs.min()), np.log10(obs.max()))

        self.titleLabel.setText('{}'.format(loc.locInd.iloc[0]))

    def setTime(self, time):
        """ docstring """
        self.selectedTimeLine.setPos(np.log10(time.values))
