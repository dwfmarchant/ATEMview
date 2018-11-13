
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
        if "moment" in self.data.df.keys():
            self.isMoment = True
            self.setSelectedMoment("H")
            self.mInd = self.data.df.moment == "H"
            self.tMaxInd = self.data.df[self.mInd].tInd.max()

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

        self.rbx = QtWidgets.QRadioButton("X component")
        self.rbx.component = "X"
        self.rbx.toggled.connect(self.on_component_toggled)
        self.rbz = QtWidgets.QRadioButton("Z Component")
        self.rbz.setChecked(True)
        self.rbz.component = "Z"
        self.rbz.toggled.connect(self.on_component_toggled)

        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.btnLoc)
        hbox1.addWidget(self.btnDecay)
        hbox1.addWidget(self.btnGrid)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.rbz)
        hbox2.addWidget(self.rbx)

        hboxes = [hbox1, hbox2]

        if self.isMoment:

            self.rblow = QtWidgets.QRadioButton("Low Moment")
            self.rblow.moment = "L"
            self.rblow.toggled.connect(self.on_moment_toggled)
            self.rbhigh = QtWidgets.QRadioButton("High Moment")
            self.rbhigh.setChecked(True)
            self.rbhigh.moment = "H"
            self.rbhigh.toggled.connect(self.on_moment_toggled)

            hbox3 = QtWidgets.QHBoxLayout()
            hbox3.addWidget(self.rblow)
            hbox3.addWidget(self.rbhigh)
            hboxes.append(hbox3)

        vbox = QtWidgets.QVBoxLayout()
        for hb in hboxes:
            vbox.addLayout(hb)

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

    def on_component_toggled(self):
        self.setSelectedComponent(self.sender().component)

    def on_moment_toggled(self):
        self.setSelectedMoment(self.sender().moment)
        self.mInd = self.data.df.moment == self.sender().moment
        self.tMaxInd = self.data.df[self.mInd].tInd.max()
        self.setSelectedTimeInd(0)

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
                self.gridWindow = GridWidget(self, self.selectedComponent)
                self.gridWindow.init_grids()
            else:
                self.gridWindow.toggleVisible()
        else:
            print('Unknown windowType: {}'.format(windowType))

        if self.isMoment:
            self.setSelectedMoment(self.selectedMoment)
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
        tInds = self.data.df[self.mInd].tInd.unique() if self.isMoment else self.data.df.tInd.unique()
        if timeInd in tInds:
            self.selectedTimeInd = timeInd
            for window in self.windows:
                if window is not None:
                    tdat = self.data.getTime(timeInd)
                    tdat = tdat[tdat.moment == self.selectedMoment] if self.isMoment else tdat
                    window.setTime(tdat)

    def setSelectedComponent(self, comp):
        """ docstring """
        self.selectedComponent = comp
        for window in self.windows:
            if window is not None:
                window.setComponent(comp)
            
    def setSelectedMoment(self, moment):
        """ docstring """
        self.selectedMoment = moment
        for window in self.windows:
            if window is not None:
                window.setMoment(moment)

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
