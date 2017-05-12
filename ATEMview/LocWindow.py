
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from Canvas import Canvas

class LocsCanvas(Canvas):
    """ Docstring """

    locClicked = pyqtSignal(dict, name='locClicked')

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """Docstring"""
        super().__init__(parent, width, height, dpi)
        self.axes.set_aspect('equal')
        
    def initPlot(self):
        """Docstring"""
        self.selPlot, = self.axes.plot([], [], 'o', c='r', ms=2.)
        self.allPlot, = self.axes.plot([], [], 'o', c='k', ms=1.)

    def onClick(self, event):
        """ Docstring """

        if event.inaxes is not None:
            signal = {'name':'locClicked',
                      'xdata':event.xdata,
                      'ydata':event.ydata}
            self.locClicked.emit(signal)

class LocWidget(QWidget):
    """docstring for LocWidget"""

    nextLocInd = pyqtSignal(dict, name='nextLocInd')
    prevLocInd = pyqtSignal(dict, name='prevLocInd')

    def __init__(self, parent):
        super(LocWidget, self).__init__()
        self.parent = parent
        self.init_ui()
        self.lc.locClicked.connect(parent.get_event)
        self.nextLocInd.connect(parent.get_event)
        self.prevLocInd.connect(parent.get_event)
        self.show()
        
    def init_ui(self):
        """ Docstring """
        self.lc = LocsCanvas(parent=self, width=5, height=4, dpi=100)        
        toolbar = NavigationToolbar(self.lc, self, coordinates=False)
        l = QVBoxLayout(self)
        l.addWidget(self.lc)
        l.addWidget(toolbar)

        self.move(50, 100)

    def setAll(self, x, y):
        """ Docstring """
        self.lc.allPlot.set_data(x, y)
        self.lc.axes.set_xlim(x.min()-100., x.max()+100.)
        self.lc.axes.set_ylim(y.min()-100., y.max()+100.)
        self.lc.draw()

    def setSel(self, x, y):
        """ Docstring """
        self.lc.selPlot.set_data(x, y)
        self.lc.draw()

    def keyPressEvent(self, event):
        """ Docstring """
        key = event.key()
        if key == Qt.Key_Right:
            print('Right Arrow Pressed')
            signal = {'name':'nextLocInd'}
            self.nextLocInd.emit(signal)
        elif key == Qt.Key_Left:
            print('Right Arrow Pressed')
            signal = {'name':'prevLocInd'}
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
