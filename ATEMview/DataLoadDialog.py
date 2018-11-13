
import os
from PyQt5 import QtWidgets, QtCore
from InvTools.ATEM import ATEMdata

class DataLoadDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, moments=False):
        super().__init__(parent=parent)

        self.data = ATEMdata()
        self.moments = moments
        self.initUI()
        self.show()

    def initUI(self):

        if self.moments:

            self.obsHText = QtWidgets.QLineEdit()
            self.obsHText.setDragEnabled(True)
            self.obsHText.setAcceptDrops(True)
            self.obsHText.installEventFilter(self)
            obsHLabel = QtWidgets.QLabel('High Moment Obs File: ')
            obsHBrowsBtn = QtWidgets.QPushButton('Browse')

            self.obsLText = QtWidgets.QLineEdit()
            self.obsLText.setDragEnabled(True)
            self.obsLText.setAcceptDrops(True)
            self.obsLText.installEventFilter(self)
            obsLLabel = QtWidgets.QLabel('Low Moment Obs File: ')
            obsLBrowsBtn = QtWidgets.QPushButton('Browse')

            self.predHText = QtWidgets.QLineEdit()
            self.predHText.setDragEnabled(True)
            self.predHText.setAcceptDrops(True)
            self.predHText.installEventFilter(self)
            predHLabel = QtWidgets.QLabel('High Moment Pred File: ')
            predHBrowsBtn = QtWidgets.QPushButton('Browse')

            self.predLText = QtWidgets.QLineEdit()
            self.predLText.setDragEnabled(True)
            self.predLText.setAcceptDrops(True)
            self.predLText.installEventFilter(self)
            predLLabel = QtWidgets.QLabel('Low Moment Pred File: ')
            predLBrowsBtn = QtWidgets.QPushButton('Browse')

            loadBtn = QtWidgets.QPushButton('Load')
            loadBtn.clicked.connect(self.loadFiles)

            ObsHLayout = QtWidgets.QHBoxLayout()
            ObsHLayout.addWidget(obsHLabel)
            ObsHLayout.addWidget(self.obsHText)
            ObsHLayout.addWidget(obsHBrowsBtn)

            PredHLayout = QtWidgets.QHBoxLayout()
            PredHLayout.addWidget(predHLabel)
            PredHLayout.addWidget(self.predHText)
            PredHLayout.addWidget(predHBrowsBtn)

            ObsLLayout = QtWidgets.QHBoxLayout()
            ObsLLayout.addWidget(obsLLabel)
            ObsLLayout.addWidget(self.obsLText)
            ObsLLayout.addWidget(obsLBrowsBtn)

            PredLLayout = QtWidgets.QHBoxLayout()
            PredLLayout.addWidget(predLLabel)
            PredLLayout.addWidget(self.predLText)
            PredLLayout.addWidget(predLBrowsBtn)

            vlayout = QtWidgets.QVBoxLayout()
            vlayout.addLayout(ObsLLayout)
            vlayout.addLayout(PredLLayout)
            vlayout.addLayout(ObsHLayout)
            vlayout.addLayout(PredHLayout)
            vlayout.addWidget(loadBtn)

            self.setLayout(vlayout)

        else:

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

        if self.moments:

            obsHFname = self.obsHText.text()
            predHFname = self.predHText.text()

            obsLFname = self.obsLText.text()
            predLFname = self.predLText.text()

            if obsHFname.startswith('file://'):
                if os.name == 'nt':
                    obsHFname = obsHFname[8:]
                elif os.name == 'posix':
                    obsHFname = obsHFname[7:]
                    obsHFname = obsHFname.strip()
                    obsHFname = obsHFname.replace('%20', ' ')
            if predHFname.startswith('file://'):
                if os.name == 'nt':
                    predHFname = predHFname[8:]
                elif os.name == 'posix':
                    predHFname = predHFname[7:]
                    predHFname = predHFname.strip()
                    predHFname = predHFname.replace('%20', ' ')

            if obsLFname.startswith('file://'):
                if os.name == 'nt':
                    obsLFname = obsLFname[8:]
                elif os.name == 'posix':
                    obsLFname = obsLFname[7:]
                    obsLFname = obsLFname.strip()
                    obsLFname = obsLFname.replace('%20', ' ')
            if predLFname.startswith('file://'):
                if os.name == 'nt':
                    predLFname = predLFname[8:]
                elif os.name == 'posix':
                    predLFname = predLFname[7:]
                    predLFname = predLFname.strip()
                    predLFname = predLFname.replace('%20', ' ')

            # self.LMdata = ATEMdata(obsLFname, predLFname)
            # self.HMdata = ATEMdata(obsHFname, predHFname)
            self.LMdata = ATEMdata('obs_rotate_lm.txt', 'dpred_006_lm.txt')
            self.HMdata = ATEMdata('obs_rotate_hm.txt', 'dpred_009_hm.txt')
            self.LMdata.df['moment'] = 'L'
            self.HMdata.df['moment'] = 'H'
            self.data = ATEMdata()
            self.data.df = self.LMdata.df.append(self.HMdata.df).reset_index(drop=True)
            self.accept()

        else:

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

            self.data = ATEMdata(obsFname, predFname)
            self.accept()

    def eventFilter(self, obj, event):
        if self.moments:
            checkobj = (obj is self.obsHText)  | \
                       (obj is self.predHText) | \
                       (obj is self.obsLText)  | \
                       (obj is self.predLText)
        else:
            checkobj = (obj is self.obsText) | \
                       (obj is self.predText)

        if checkobj:
            if (event.type() == QtCore.QEvent.DragEnter):
                if event.mimeData().hasUrls():
                    event.accept()
                else:
                    event.ignore()
            return False # lets the event continue to the edit
        return False
