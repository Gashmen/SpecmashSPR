from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog
import sys

class Ui_ShellError(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Error Window')
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ShellError_label = QtWidgets.QLabel()
        self.ShellError_label.setText('НЕТ ДАННОЙ ОБОЛОЧКИ В БАЗЕ DXF')
        self.horizontalLayout.addWidget(self.ShellError_label)
        QtCore.QMetaObject.connectSlotsByName(self)


    def call_shellerror(self):
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_ShellError()
    window.call_shellerror()
    sys.exit(app.exec_())
