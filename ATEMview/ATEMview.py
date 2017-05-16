
import sys
from PyQt5.QtWidgets import QApplication

from MainWindow import ATEMViewMainWindow
from DataLoadDialog import DataLoadDialog

def main(data=None):
    app = QApplication(sys.argv)
    if data is None:
        dataLoader = DataLoadDialog()
        dataLoader.exec_()
        data = dataLoader.data
    else:
        data = data

    ATEM = ATEMViewMainWindow(data)
    app.exec_()

if __name__ == '__main__':
    main()
