"""
ATEMview launcher
"""
import sys
from PyQt5 import QtWidgets
from MainWindow import ATEMViewMainWindow
from DataLoadDialog import DataLoadDialog

def main(data=None):
    """
    ATEMview launcher
    """
    app = QtWidgets.QApplication(sys.argv)
    if data is None:
        dataLoader = DataLoadDialog()
        dataLoader.exec_()
        data = dataLoader.data
    else:
        data = data
    atem = ATEMViewMainWindow(data)
    print(atem)
    app.exec_()

if __name__ == '__main__':
    main()
