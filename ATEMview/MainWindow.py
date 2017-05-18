
from PyQt5 import QtCore, QtWidgets
from LocWindow import LocWidget
from DecayWindow import DecayWidget
from GridWindow import GridWidget

class ATEMViewMainWindow(QtWidgets.QMainWindow):
    """ Docstring """

    selectedLocInd = -1
    selectedTimeInd = -1

    LocWindow = None
    DecayWindow = None
    GridWindow = None

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
        self.btnLoc.clicked.connect(self.buttonClicked)
        self.btnDecay.clicked.connect(self.buttonClicked)
        self.btnGrid.clicked.connect(self.buttonClicked)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.btnLoc)
        hbox.addWidget(self.btnDecay)
        hbox.addWidget(self.btnGrid)
        self.main_widget.setLayout(hbox)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("", 2000)

    def buttonClicked(self):
        """ Docstring """
        if self.sender() is self.btnLoc:
            self.openLocWindow()
        elif self.sender() is self.btnDecay:
            self.openDecayWindow()
        elif self.sender() is self.btnGrid:
            self.openGridWindow()

    def closeEvent(self, event):
        for window in [self.LocWindow, self.DecayWindow, self.GridWindow]:
            if window is not None:
                window.deleteLater()
                window = None
        event.accept()

    def openLocWindow(self):
        """ docstring """
        if self.LocWindow is None:
            self.LocWindow = LocWidget(self)
            self.LocWindow.setAll(self.data.locs.x.values,
                                  self.data.locs.y.values)
            self.setSelectedLocInd(self.selectedLocInd)
            self.setSelectedTimeInd(self.selectedTimeInd)
        else:
            self.LocWindow.toggleVisible()

    def openDecayWindow(self):
        """ docstring """
        if self.DecayWindow is None:
            self.DecayWindow = DecayWidget(self)
            self.setSelectedLocInd(self.selectedLocInd)
            self.setSelectedTimeInd(self.selectedTimeInd)
        else:
            self.DecayWindow.toggleVisible()

    def openGridWindow(self):
        """ docstring """
        if self.GridWindow is None:
            self.GridWindow = GridWidget(self)
            self.setSelectedLocInd(self.selectedLocInd)
            self.setSelectedTimeInd(self.selectedTimeInd)
        else:
            self.GridWindow.toggleVisible()

    def setSelectedLocInd(self, locInd):
        """ docstring """
        if locInd in self.data.locs.index:
            self.selectedLocInd = locInd
            selectedLoc = self.data.getLoc(locInd)

            if self.LocWindow is not None:
                self.LocWindow.setLocation(selectedLoc)
            if self.DecayWindow is not None:
                self.DecayWindow.setLocation(selectedLoc)
            if self.GridWindow is not None:
                self.GridWindow.setLocation(selectedLoc)

    def setSelectedTimeInd(self, timeInd):
        """ docstring """

        if timeInd in self.data.times.index:
            self.selectedTimeInd = timeInd
            if self.GridWindow is not None:
                self.GridWindow.setTime(self.data.getTime(timeInd))
            if self.DecayWindow is not None:
                self.DecayWindow.setTime(self.data.times.loc[timeInd])

    @QtCore.pyqtSlot(dict)
    def get_event(self, event):
        """ docstring """

        if event['name'] == 'closestLoc':
            closestLoc = self.data.getClosestLocInd(event['x'], event['y'])
            self.setSelectedLocInd(closestLoc)
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
