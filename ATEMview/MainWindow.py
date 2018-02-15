
from PyQt5 import QtCore, QtWidgets
from .LocWindow import LocWidget
from .DecayWindow import DecayWidget
from .GridWindow import GridWidget

class ATEMViewMainWindow(QtWidgets.QMainWindow):
    """ Docstring """

    selectedLocInd = 0
    selectedTimeInd = 0
    # selectedComponent = "Z"

    locWindow = None
    decayWindow = None
    gridWindow = None

    def __init__(self, data):
        QtWidgets.QMainWindow.__init__(self)

        self.data = data

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.initUI()

        # Initialize the selection
        self.setSelectedLocInd(self.data.locs.iloc[0].name)
        self.setSelectedTimeInd(self.data.times.iloc[0].name)
        self.setSelectedComponent("Z")

        # # Initialize z component selection (matches default radio selection)
        # self.active_component = "Z"

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

        self.rbx = QtWidgets.QRadioButton("x")
        self.rbx.component = "X"
        self.rbx.toggled.connect(self.on_radio_button_toggled)
        self.rbz = QtWidgets.QRadioButton("z")
        self.rbz.setChecked(True)
        self.rbz.component = "Z"
        self.rbz.toggled.connect(self.on_radio_button_toggled)

        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.btnLoc)
        hbox1.addWidget(self.btnDecay)
        hbox1.addWidget(self.btnGrid)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.rbz)
        hbox2.addWidget(self.rbx)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.main_widget.setLayout(vbox)

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

    def on_radio_button_toggled(self):
        self.setSelectedComponent(self.sender().component)
        # self.active_component = self.sender().component



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
                self.setSelectedComponent(self.selectedComponent)
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
                self.setSelectedComponent(self.selectedComponent)
                self.gridWindow.init_grids()
            else:
                self.gridWindow.toggleVisible()
        else:
            print('Unknown windowType: {}'.format(windowType))

        self.setSelectedComponent(self.selectedComponent)
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

    def setSelectedComponent(self, comp):
        """ docstring """
        self.selectedComponent = comp
        for window in self.windows:
            if window is not None:
                window.setComponent(comp)


    @property
    def windows(self):
        """ Return a list of accosiated windows """
        return [self.locWindow, self.decayWindow, self.gridWindow]

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
