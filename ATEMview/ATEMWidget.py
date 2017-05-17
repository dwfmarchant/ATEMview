
from PyQt5 import QtWidgets, QtCore

class ATEMWidget(QtWidgets.QWidget):
    """docstring for ATEMWidget."""

    ChangeSelectionSignal = QtCore.pyqtSignal(dict, name='ChangeSelection')

    def __init__(self, parent):
        super(ATEMWidget, self).__init__()
        self.ChangeSelectionSignal.connect(parent.get_event)

    def toggleVisible(self):
        """ Toggle widget visiblity """
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def keyPressEvent(self, event):
        """ Docstring """
        key = event.key()
        if key == QtCore.Qt.Key_Right:
            signal = {'name':'nextLocInd'}
        elif key == QtCore.Qt.Key_Left:
            signal = {'name':'prevLocInd'}
        elif key == QtCore.Qt.Key_Up:
            signal = {'name':'nextTimeInd'}
        elif key == QtCore.Qt.Key_Down:
            signal = {'name':'prevTimeInd'}
        else:
            return
        self.ChangeSelectionSignal.emit(signal)
