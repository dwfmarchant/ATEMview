"""
ATEMview launcher
"""
import sys
from optparse import OptionParser
from PyQt5 import QtWidgets
from ATEMview.MainWindow import ATEMViewMainWindow
from ATEMview.DataLoadDialog import DataLoadDialog

def startATEMview(data=None, moments=False):
    """
    ATEMview launcher
    """
    
    app = QtWidgets.QApplication(sys.argv)

    if data is None:
        if moments:
            dataLoader = DataLoadDialog(moments=True)
            dataLoader.exec_()
            data = dataLoader.data
            atem = ATEMViewMainWindow(data)
        else:
            dataLoader = DataLoadDialog()
            dataLoader.exec_()
            data = dataLoader.data
            atem = ATEMViewMainWindow(data)

    else:
        data = data
        atem = ATEMViewMainWindow(data)

    
    # print(atem)
    app.exec_()

if __name__ == '__main__':
    startATEMview()
