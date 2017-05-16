import sys
from PyQt5.QtWidgets import (QDialog, QPushButton, QLineEdit,
                             QLabel, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QEvent
from InvTools.ATEM import ATEMdata

class DataLoadDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.initUI()
        self.show()

    def initUI(self):

        self.obsText = QLineEdit()
        self.obsText.setDragEnabled(True)
        self.obsText.setAcceptDrops(True)
        self.obsText.installEventFilter(self)

        obsLabel = QLabel('Obs File: ')
        obsBrowsBtn = QPushButton('Browse')


        self.predText = QLineEdit()
        self.predText.setDragEnabled(True)
        self.predText.setAcceptDrops(True)
        self.predText.installEventFilter(self)
        predLabel = QLabel('Pred File: ')
        predBrowsBtn = QPushButton('Browse')

        loadBtn = QPushButton('Load')
        loadBtn.clicked.connect(self.loadFiles)

        ObsLayout = QHBoxLayout()
        ObsLayout.addWidget(obsLabel)
        ObsLayout.addWidget(self.obsText)
        ObsLayout.addWidget(obsBrowsBtn)

        PredLayout = QHBoxLayout()
        PredLayout.addWidget(predLabel)
        PredLayout.addWidget(self.predText)
        PredLayout.addWidget(predBrowsBtn)

        vlayout = QVBoxLayout()
        vlayout.addLayout(ObsLayout)
        vlayout.addLayout(PredLayout)
        vlayout.addWidget(loadBtn)

        self.setLayout(vlayout)

    def loadFiles(self, event):
        obsFname = self.obsText.text()
        predFname = self.predText.text()

        if obsFname.startswith('file://'):
            obsFname = obsFname[7:]
        if predFname.startswith('file://'):
            predFname = predFname[7:]

        self.data = ATEMdata(obsFname, predFname)
        self.accept()

    def eventFilter(self, object, event):
        if (object is self.obsText) | (object is self.predText):
            if (event.type() == QEvent.DragEnter):
                if event.mimeData().hasUrls():
                    event.accept()
                else:
                    event.ignore()
            return False # lets the event continue to the edit
        return False
