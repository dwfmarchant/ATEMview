
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, Qt

class ATEMWidget(QWidget):
    """docstring for ATEMWidget."""

    keyPressSignal = pyqtSignal(dict, name='keyPress')

    def __init__(self, parent):
        super(ATEMWidget, self).__init__()
        self.keyPressSignal.connect(parent.get_event)

    def toggleVisible(self):
        """ Toggle widget visiblity """
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def keyPressEvent(self, event):
        """ Docstring """
        key = event.key()
        if key == Qt.Key_Right:
            signal = {'name':'nextLocInd'}
        elif key == Qt.Key_Left:
            signal = {'name':'prevLocInd'}
        elif key == Qt.Key_Up:
            signal = {'name':'nextTimeInd'}
        elif key == Qt.Key_Down:
            signal = {'name':'prevTimeInd'}
        else:
            return
        self.keyPressSignal.emit(signal)
