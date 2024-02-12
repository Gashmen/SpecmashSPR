from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog
import sys

class Ui_BaseError(QDialog):
    def __init__(self,text_base_error='НЕТ ДАННОЙ ОБОЛОЧКИ В БАЗЕ DXF'):
        super().__init__()
        self.setWindowTitle('Error Window')
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ShellError_label = QtWidgets.QLabel()
        self.ShellError_label.setText(text_base_error)
        self.horizontalLayout.addWidget(self.ShellError_label)
        QtCore.QMetaObject.connectSlotsByName(self)


    def call_error(self):
        self.open()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_BaseError()
    window.call_error()
    sys.exit(app.exec_())
