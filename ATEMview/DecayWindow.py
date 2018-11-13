
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

        self.lockYRange = False
        self.plotYmin = 1.
        self.plotYmax = 2.
        self.dataYmin = 1.
        self.dataYmax = 2.

        self.init_ui()
        self.show()

    def initGraph(self, name=False):
            graphItems = {}
            graphItems['obsPlot'] = pg.PlotDataItem(symbol='o',
                                                    symbolSize=5,
                                                    symbolBrush='k',
                                                    pen={'color': 'k',
                                                        'width': 2},
                                                    name = 'Obs.' if name else None)

            graphItems['obsNegPlot'] = pg.PlotDataItem(symbol='o',
                                                        symbolSize=5,
                                                        symbolBrush='r',
                                                        pen=None,
                                                        name=None)

            graphItems['predPlot'] = pg.PlotDataItem(symbol='o',
                                                    symbolSize=5,
                                                    symbolBrush='b',
                                                    pen={'color': 'b',
                                                        'width': 2},
                                                    name='Pred.' if name else None)

            graphItems['predNegPlot'] = pg.PlotDataItem(symbol='o',
                                                        symbolSize=12,
                                                        symbolBrush='m',
                                                        pen=None,
                                                        name=None)

            graphItems['lowerPlot'] = pg.PlotDataItem()
            graphItems['upperPlot'] = pg.PlotDataItem()
            graphItems['uncertBounds'] = pg.FillBetweenItem(graphItems['lowerPlot'], graphItems['upperPlot'], 0.8)


            return graphItems
    
    def init_ui(self):
        """ Docstring """

        # Make the background white
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(palette)

        self.titleLabel = QtWidgets.QLabel()
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        self.locLabel = QtWidgets.QLabel('')
        self.locLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.optLabel = QtWidgets.QLabel('')
        self.optLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setLogMode(x=True, y=True)
        self.plotWidget.setLabel('left', 'dB/dt')
        self.plotWidget.setLabel('bottom', 'Time', units='s')
        legend = self.plotWidget.addLegend(offset=(450, 30))
        self.plotWidget.showGrid(x=True, y=True)

        if self.parent.isMoment:
            self.graphItems = {'L':self.initGraph(name=True), 'H':self.initGraph()} # [low moment, high moment]
        else:
            self.graphItems = {'N':self.initGraph()}

     


        self.selectedTimeLine = pg.InfiniteLine(angle=90,
                                                movable=False,
                                                pen={'color': 'k',
                                                     'width': 2,
                                                     'style': QtCore.Qt.DotLine})

        # Crosshair
        self.chvLine = pg.InfiniteLine(angle=90, movable=False, pen={'color':'k', 'width':0.25})
        self.chhLine = pg.InfiniteLine(angle=0, movable=False, pen={'color':'k', 'width':0.25})

        self.plotWidget.addItem(self.chvLine, ignoreBounds=True)
        self.plotWidget.addItem(self.chhLine, ignoreBounds=True)
        self.plotWidget.addItem(self.selectedTimeLine, ignoreBounds=True)

        for gi in self.graphItems.values():
            for v in gi.values():
                self.plotWidget.addItem(v)

        # uncertBounds.setZValue(0)
        # self.selectedTimeLine.setZValue(1)
        # self.obsNegPlot.setZValue(3)
        # self.obsPlot.setZValue(2)
        # self.predNegPlot.setZValue(5)
        # self.predPlot.setZValue(4)
        # self.chvLine.setZValue(6)
        # self.chhLine.setZValue(7)
        # legend.setZValue(7)np.abs(obs)

        l = QtWidgets.QVBoxLayout(self)
        l.addWidget(self.titleLabel)
        l.addWidget(self.plotWidget)
        labelBox = QtWidgets.QHBoxLayout()
        labelBox.addWidget(self.optLabel)
        labelBox.addWidget(self.locLabel)
        l.addLayout(labelBox)

        self.mouseMoveProxy = pg.SignalProxy(self.plotWidget.scene().sigMouseMoved,
                                             rateLimit=30,
                                             slot=self.mouseMovedEvent)
        self.plotWidget.scene().sigMouseClicked.connect(self.clickEvent)

    def keyPressEvent(self, event):
        """ Docstring """
        key = event.key()
        if key == QtCore.Qt.Key_Right:
            signal = {'name':'nextLocInd'}
        elif key == QtCore.Qt.Key_Left:
            signal = {'name':'prevLocInd'}
        elif key == QtCore.Qt.Key_Up:
            signal = {'name':'nextTimeInd'}
        elif key == QtCore.Qt.Key_Down:
            signal = {'name':'prevTimeInd'}
        elif key == QtCore.Qt.Key_L:
            if self.lockYRange:
                self.lockYRange = False
            else:
                self.lockYRange = True
            self.updateOptLabel()
            self.updateYRange()
            return
        elif key == QtCore.Qt.Key_R:
            self.updateYRange(rescale=True)
            return
        else:
            return
        self.ChangeSelectionSignal.emit(signal)

    def mouseMovedEvent(self, pos):
        pos = pos[0]
        if self.plotWidget.sceneBoundingRect().contains(pos):
            mousePoint = self.plotWidget.getViewBox().mapSceneToView(pos)
            string = "<span style='font-size: 12pt'>t={:.2e}</span>"
            self.locLabel.setText(string.format(10**mousePoint.x()))
            self.chvLine.setPos(mousePoint.x())
            self.chhLine.setPos(mousePoint.y())

    def clickEvent(self, event):
        if self.plotWidget.sceneBoundingRect().contains(event.scenePos()):
            mousePoint = self.plotWidget.getViewBox().mapSceneToView(event.scenePos())
            signal = {'name':'closestTime',
                      't':10**mousePoint.x()}
            self.ChangeSelectionSignal.emit(signal)
        else:
            pass

    def setLocation(self, loc):
        """ Docstring """
        
        for gi, gv in self.graphItems.items():
            
            for k, g in gv.items():

                if gi == 'N':
                    t = loc.t.values
                    obs = loc[self.ach]
                    pred = loc[self.ach + '_pred']
                    uncert = loc[self.ach + '_uncert']
                    lower = obs.abs().values - uncert.values
                    upper = obs.abs().values + uncert.values
                else:
                    Mloc = loc[loc["moment"] == gi]
                    t = Mloc.t.values
                    obs = Mloc[self.ach]
                    pred = Mloc[self.ach + '_pred']
                    uncert = Mloc[self.ach + '_uncert']
                    lower = obs.abs().values - uncert.values
                    upper = obs.abs().values + uncert.values

                if k == 'obsPlot':
                    g.setData(t, obs.abs().values)
                elif k == 'obsNegPlot':
                    nInd = obs.values < 0.
                    g.setData(t[nInd], obs.abs().values[nInd])
                elif k == 'predPlot':
                    if pred.any():
                        g.setData(t, pred.abs().values)
                elif k == 'predNegPlot':
                    if pred.any():
                        nInd = pred.values < 0.
                        g.setData(t[nInd], pred.abs().values[nInd])
                elif k == 'upperPlot':
                    if loc[self.ach + '_uncert'].any():
                        ignore_ind = obs != -9999
                        g.setData(t[ignore_ind], upper[ignore_ind])
                elif k == 'lowerPlot':
                    if loc[self.ach + '_uncert'].any():
                        ignore_ind = obs != -9999
                        lower[lower < 0.] = obs.abs().min()/100.
                        g.setData(t[ignore_ind], lower[ignore_ind])

        self.plotWidget.setXRange(np.log10(loc.t.min()), np.log10(loc.t.max()))
        self.updateYRange(yMin=np.log10(loc[self.ach].abs().min()),
                          yMax=np.log10(loc[self.ach].abs().max()))

        self.titleLabel.setText('{}'.format(loc.locInd.iloc[0]))

    def updateYRange(self, yMin=None, yMax=None, rescale=False):
        if yMin is not None:
            self.dataYmin = yMin
        if yMax is not None:
            self.dataYmax = yMax
        if not self.lockYRange:
            self.plotYmin = self.dataYmin
            self.plotYmax = self.dataYmax
        if rescale:
            if self.dataYmin < self.plotYmin:
                self.plotYmin = self.dataYmin
            if self.dataYmax > self.plotYmax:
                self.plotYmax = self.dataYmax
        self.plotWidget.setYRange(self.plotYmin, self.plotYmax)

    def setTime(self, time):
        """ docstring """
        if self.isMoment:
            Mtime = time[time.moment == self.selectedMoment]
            t = Mtime.iloc[0].t
        else:
            t = time.iloc[0].t
        self.selectedTimeLine.setPos(np.log10(t))

    def setComponent(self, component):
        self.ach = 'dBdt_' + component # switch active channel

    def setMoment(self, moment):
        self.isMoment = True
        self.selectedMoment = moment

    def updateOptLabel(self):
        if self.lockYRange:
            self.optLabel.setText("Lock Y-Range")
        else:
            self.optLabel.setText("")
