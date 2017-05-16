
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QPushButton, QHBoxLayout)

class MainWindow(QMainWindow):
    """ Docstring """
    def __init__(self, parent):
        QMainWindow.__init__(self)

        self.parent = parent

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.initUI()

        self.btnLoc.clicked.connect(self.buttonClicked)
        self.btnDecay.clicked.connect(self.buttonClicked)
        self.btnGrid.clicked.connect(self.buttonClicked)

    def initUI(self):
        """ Docstring """
        self.setWindowTitle("application main window")

        self.main_widget = QWidget(self)

        self.btnLoc = QPushButton("Loc")
        self.btnDecay = QPushButton("Decay")
        self.btnGrid = QPushButton("Grid")

        hbox = QHBoxLayout()
        hbox.addWidget(self.btnLoc)
        hbox.addWidget(self.btnDecay)
        hbox.addWidget(self.btnGrid)
        self.main_widget.setLayout(hbox)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("", 2000)

    def buttonClicked(self):
        """ Docstring """
        sender = self.sender()
        if sender.text() == "Loc":
            self.parent.openLocWindow()
        elif sender.text() == "Decay":
            self.parent.openDecayWindow()
        elif sender.text() == "Grid":
            self.parent.openGridWindow()


if __name__ == '__main__':

    from InvTools.ATEM import ATEMdata
    from ATEMview import ATEMviewer

    # obsFile = '/Users/dmarchant/Dropbox (CGI)/Projects2017/BlackwellHPX/Inv/20170512/Inv12_Blk1_R1/run2/obs.txt'
    # predFile = '/Users/dmarchant/Dropbox (CGI)/Projects2017/BlackwellHPX/Inv/20170512/Inv12_Blk1_R1/run2/dpred.txt'
    # dat = ATEMdata(obsFile, predFile)
    dat = ATEMdata()
    dat.readPkl('/Users/dmarchant/Dropbox (CGI)/Projects2017/BlackwellHPX/Inv/20170512/Inv12_Blk1_R1/run2/ATEM.pkl')

    app = QApplication(sys.argv)
    ATEM = ATEMviewer(dat)

    # aw = ApplicationWindow(dat)
    # aw.setWindowTitle("PyQt5 Matplot Example")
    # aw.show()
    app.exec_()
