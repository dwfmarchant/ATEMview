
from PyQt5 import QtCore, QtWidgets
from .LocWindow import LocWidget
from .DecayWindow import DecayWidget
from .GridWindow import GridWidget
from .LineWindow import LineWidget

class ATEMViewMainWindow(QtWidgets.QMainWindow):
    """ Docstring """

    selectedLocInd = 0
    selectedTimeInd = 0

    locWindow = None
    decayWindow = None
    gridWindow = None
    lineWindow = None

    def __init__(self, data):
        QtWidgets.QMainWindow.__init__(self)

        self.data = data

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.initUI()

        # Initialize the selection
        self.setSelectedLocInd(self.data.locs.iloc[0].name)
        self.setSelectedTimeInd(self.data.times.iloc[0].name)

        self.show()

    def initUI(self):
        """ Docstring """
        self.setWindowTitle("application main window")

        self.main_widget = QtWidgets.QWidget(self)

        self.btnLoc = QtWidgets.QPushButton("Loc")
        self.btnDecay = QtWidgets.QPushButton("Decay")
        self.btnGrid = QtWidgets.QPushButton("Grid")
        self.btnLine = QtWidgets.QPushButton("Line")

        self.btnLoc.clicked.connect(self.buttonClicked)
        self.btnDecay.clicked.connect(self.buttonClicked)
        self.btnGrid.clicked.connect(self.buttonClicked)
        self.btnLine.clicked.connect(self.buttonClicked)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.btnLoc)
        hbox.addWidget(self.btnDecay)
        hbox.addWidget(self.btnGrid)
        hbox.addWidget(self.btnLine)
        self.main_widget.setLayout(hbox)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("", 2000)

    def buttonClicked(self):
        """ Docstring """
        if self.sender() is self.btnLoc:
            self.openWindow('Loc')
        elif self.sender() is self.btnDecay:
            self.openWindow('Decay')
        elif self.sender() is self.btnGrid:
            self.openWindow('Grid')
        elif self.sender() is self.btnLine:
            self.openWindow('Line')

    def closeEvent(self, event):
        """
        closeEvent for MainWindow
        Closes all open windows.
        """
        for window in [self.locWindow, self.decayWindow, self.gridWindow]:
            if window is not None:
                window.deleteLater()
                window = None
        event.accept()

    def openWindow(self, windowType):
        if windowType is 'Loc':
            if self.locWindow is None:
                self.locWindow = LocWidget(self)
                self.locWindow.setAll(self.data.locs.x.values,
                                      self.data.locs.y.values)
            else:
                self.locWindow.toggleVisible()
        elif windowType is 'Decay':
            if self.decayWindow is None:
                self.decayWindow = DecayWidget(self)
            else:
                self.decayWindow.toggleVisible()
        elif windowType is 'Grid':
            if self.gridWindow is None:
                self.gridWindow = GridWidget(self)
            else:
                self.gridWindow.toggleVisible()
        elif windowType is 'Line':
            if self.lineWindow is None:
                self.lineWindow = LineWidget(self)
            else:
                self.lineWindow.toggleVisible()
        else:
            print('Unknown windowType: {}'.format(windowType))

        self.setSelectedLocInd(self.selectedLocInd)
        self.setSelectedTimeInd(self.selectedTimeInd)

    def setSelectedLocInd(self, locInd):
        """ docstring """
        if locInd in self.data.locs.index:
            self.selectedLocInd = locInd
            selectedLoc = self.data.getLoc(locInd)
            for window in self.windows:
                if window is not None:
                    window.setLocation(selectedLoc)

    def setSelectedTimeInd(self, timeInd):
        """ docstring """
        if timeInd in self.data.times.index:
            self.selectedTimeInd = timeInd
            for window in self.windows:
                if window is not None:
                    window.setTime(self.data.getTime(timeInd))

    @property
    def windows(self):
        """ Return a list of accosiated windows """
        return [self.locWindow, self.decayWindow, self.gridWindow, self.lineWindow]

    @QtCore.pyqtSlot(dict)
    def get_event(self, event):
        """ docstring """
        if event['name'] == 'closestLoc':
            closestLocInd = self.data.getClosestLocInd(event['x'], event['y'])
            self.setSelectedLocInd(closestLocInd)
        elif event['name'] == 'closestTime':
            closestTimeInd = self.data.getClosestTimeInd(event['t'])
            self.setSelectedTimeInd(closestTimeInd)
        elif event['name'] == 'sameTime':
            self.setSelectedTimeInd(self.selectedTimeInd)
        elif event['name'] == 'nextLocInd':
            self.setSelectedLocInd(self.selectedLocInd + 1)
        elif event['name'] == 'prevLocInd':
            self.setSelectedLocInd(self.selectedLocInd - 1)
        elif event['name'] == 'nextTimeInd':
            self.setSelectedTimeInd(self.selectedTimeInd + 1)
        elif event['name'] == 'prevTimeInd':
            self.setSelectedTimeInd(self.selectedTimeInd - 1)
        else:
            print(event['name'])
