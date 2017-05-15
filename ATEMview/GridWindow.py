
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class GridCanvas(FigureCanvas):
    """ Docstring """

    locClicked = pyqtSignal(dict, name='locClicked')

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """ Docstring """

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.obs_axes = fig.add_subplot(121)
        self.pred_axes = fig.add_subplot(122)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.mpl_connect('button_press_event', self.onClick)

        self.obs_axes.set_aspect('equal')
        self.pred_axes.set_aspect('equal')

        self.draw()


    def showGrid(self, xv, yv, GrdObs, GrdPred):
        """Docstring"""
        self.obs_axes.cla()
        self.obs_axes.contourf(xv, yv, GrdObs)

        self.pred_axes.cla()
        self.pred_axes.contourf(xv, yv, GrdPred)
        self.draw()

    def onClick(self, event):
        """ Docstring """
        if event.inaxes is not None:
            signal = {'name':'locClicked',
                      'xdata':event.xdata,
                      'ydata':event.ydata}
            self.locClicked.emit(signal)

class GridWidget(QWidget):
    """docstring for GridWidget"""

    nextLocInd = pyqtSignal(dict, name='nextLocInd')
    prevLocInd = pyqtSignal(dict, name='prevLocInd')

    def __init__(self, parent):
        super(GridWidget, self).__init__()
        self.parent = parent
        self.init_ui()
        self.gc.locClicked.connect(parent.get_event)
        self.nextLocInd.connect(parent.get_event)
        self.prevLocInd.connect(parent.get_event)
        self.show()

    def init_ui(self):
        """ Docstring """
        self.gc = GridCanvas(parent=self, width=10, height=4, dpi=100)
        toolbar = NavigationToolbar(self.gc, self, coordinates=False)
        l = QVBoxLayout(self)
        l.addWidget(self.gc)
        l.addWidget(toolbar)

        # self.move(50, 3000)
        self.move(-1500, 200)

    def toggleVisible(self):
        """ docstring """
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def setGrid(self, xv, yv, GrdObs, GrdPred):
        self.gc.showGrid(xv, yv, GrdObs, GrdPred)

    # def setSel(self, x, y):
    #     """ Docstring """
    #     self.gc.selPlot.set_data(x, y)
    #     self.gc.draw()

    def keyPressEvent(self, event):
        """ Docstring """
        key = event.key()
        if key == Qt.Key_Right:
            signal = {'name':'nextLocInd'}
            self.nextLocInd.emit(signal)
        elif key == Qt.Key_Left:
            signal = {'name':'prevLocInd'}
            self.prevLocInd.emit(signal)
        elif key == Qt.Key_Up:
            signal = {'name':'nextTimeInd'}
            self.prevLocInd.emit(signal)
        elif key == Qt.Key_Down:
            signal = {'name':'prevTimeInd'}
            self.prevLocInd.emit(signal)


if __name__ == '__main__':


    from PyQt5.QtWidgets import QApplication
    from ATEMview import ATEMviewer
    from InvTools.ATEM import ATEMdata

    obsFile = '/Users/dmarchant/Dropbox (CGI)/Projects2017/BlackwellHPX/Inv/20170425/Inv1_HMprelim/obs.txt'
    predFile = '/Users/dmarchant/Dropbox (CGI)/Projects2017/BlackwellHPX/Inv/20170425/Inv1_HMprelim/dpred.txt'

    dat = ATEMdata(obsFile, predFile)

    app = QApplication([])
    ATEM = ATEMviewer(dat)
    app.exec_()
