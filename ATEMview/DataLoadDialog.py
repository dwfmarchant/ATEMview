
import os
from PyQt5 import QtWidgets, QtCore
from InvTools.ATEM import ATEMdata

class DataLoadDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.data = ATEMdata()
        self.initUI()
        self.show()

    def initUI(self):

        self.obsText = QtWidgets.QLineEdit()
        self.obsText.setDragEnabled(True)
        self.obsText.setAcceptDrops(True)
        self.obsText.installEventFilter(self)

        obsLabel = QtWidgets.QLabel('Obs File: ')
        obsBrowsBtn = QtWidgets.QPushButton('Browse')


        self.predText = QtWidgets.QLineEdit()
        self.predText.setDragEnabled(True)
        self.predText.setAcceptDrops(True)
        self.predText.installEventFilter(self)
        predLabel = QtWidgets.QLabel('Pred File: ')
        predBrowsBtn = QtWidgets.QPushButton('Browse')

        loadBtn = QtWidgets.QPushButton('Load')
        loadBtn.clicked.connect(self.loadFiles)

        ObsLayout = QtWidgets.QHBoxLayout()
        ObsLayout.addWidget(obsLabel)
        ObsLayout.addWidget(self.obsText)
        ObsLayout.addWidget(obsBrowsBtn)

        PredLayout = QtWidgets.QHBoxLayout()
        PredLayout.addWidget(predLabel)
        PredLayout.addWidget(self.predText)
        PredLayout.addWidget(predBrowsBtn)

        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addLayout(ObsLayout)
        vlayout.addLayout(PredLayout)
        vlayout.addWidget(loadBtn)

        self.setLayout(vlayout)

    def loadFiles(self):
        obsFname = self.obsText.text()
        predFname = self.predText.text()

        if obsFname.startswith('file://'):
            if os.name=='nt':
                obsFname = obsFname[8:]
            elif os.name=='posix':
                obsFname = obsFname[7:]
                obsFname = obsFname.strip()
                obsFname = obsFname.replace('%20', ' ')
        if predFname.startswith('file://'):
            if os.name=='nt':
                predFname = predFname[8:]
            elif os.name=='posix':
                predFname = predFname[7:]
                predFname = predFname.strip()
                predFname = predFname.replace('%20', ' ')




        # if obsFname.startswith('\nfile://'):
        #     if os.name=='nt':
        #         obsFname = obsFname[10:]
        #     elif os.name=='posix':
        #         obsFname = obsFname[9:]
        # if predFname.startswith('\nfile://'):
        #     if os.name=='nt':
        #         predFname = predFname[10:]
        #     elif os.name=='posix':
        #         predFname = predFname[9:]

        self.data = ATEMdata(obsFname, predFname)
        self.accept()

    def eventFilter(self, obj, event):
        if (obj is self.obsText) | (obj is self.predText):
            if (event.type() == QtCore.QEvent.DragEnter):
                if event.mimeData().hasUrls():
                    event.accept()
                else:
                    event.ignore()
            return False # lets the event continue to the edit
        return False
