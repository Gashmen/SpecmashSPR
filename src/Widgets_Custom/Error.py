from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog


class Ui_WidgetError(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Error Window')
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Error_listwidget = QtWidgets.QListWidget()
        self.Error_listwidget.setObjectName("Error_listwidget")
        self.horizontalLayout.addWidget(self.Error_listwidget)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, WidgetError):
        _translate = QtCore.QCoreApplication.translate
        WidgetError.setWindowTitle(_translate("WidgetError", "Form"))

    def add_error(self, str_error):
        self.Error_listwidget.addItem(str_error)

    def call_error(self):
        self.show()



