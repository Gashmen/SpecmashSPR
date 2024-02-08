import random
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, Qt

class Ellipse():
    def __init__(self):
        self.rect = QtCore.QRect()
        self.drag_position = QtCore.QPoint()



class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.rect = QtCore.QRect()
        self.drag_position = QtCore.QPoint()

        button = QtWidgets.QPushButton("Add", self)
        button.clicked.connect(self.on_clicked)

        self.resize(640, 480)

    @QtCore.pyqtSlot()
    def on_clicked(self):
        # if self.rect.isNull():
            random_input = random.sample(range(50), 1)[0]

            if self.rect.isNull():
                self.rect = QtCore.QRect(
                    QtCore.QPoint(*random.sample(range(400), 2)), QtCore.QSize(random_input,random_input)
                )
                self.update()



    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.rect.isNull():
            painter = QtGui.QPainter(self)
            # painter.setRenderHint(QtGui.QPainter.Antialiasing)
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 0.5, QtCore.Qt.SolidLine))
            painter.drawEllipse(self.rect)#Строит окружность
            painter.drawText(self.rect, QtCore.Qt.AlignCenter, 'Center')#Можно написать название кабельного ввода по центру


    def mousePressEvent(self, event):
        if (
            2 * QtGui.QVector2D(event.pos() - self.rect.center()).length()
            < self.rect.width()):
            self.drag_position = event.pos() - self.rect.topLeft()
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        print(event.pos())
        super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):
        if not self.drag_position.isNull():
            print(event.pos())
            # print(self.drag_position.x())
            self.rect.moveTopLeft(event.pos() - self.drag_position)
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drag_position = QtCore.QPoint()
        super().mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Rect = Window()
    Rect.show()
    sys.exit(app.exec_())

