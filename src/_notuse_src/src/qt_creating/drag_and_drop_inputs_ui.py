import random
import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPointF,QRect,QPoint,QSize


class MovingObject(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        random_input = random.sample(range(50), 1)[0]
        # self.rect = QRect(QPoint(*random.sample(range(400), 2)), QSize(random_input,random_input))
        # self.update()

        # self.drag_position = QPoint()
        self.setPos(x, y)
        self.setPen(Qt.blue)
        self.setAcceptHoverEvents(True)
        self.text = QGraphicsTextItem(self)
        # self.text.setPlainText('123')
        # self.text.setPos(self.pos())

    # mouse hover event
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        # if (
        #     2 * QtGui.QVector2D(event.pos() - self.rect.center()).length()
        #     < self.rect.width()):
        #     self.drag_position = event.pos() - self.rect.topLeft()
        # super().mousePressEvent(event)
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
        self.text.setPos(self.pos())

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

class StaySurface(QGraphicsRectItem):
    def __init__(self,x, y, w, h):
        super().__init__(100,100,300,300)
        self.setPos(x, y)
        self.setPen(Qt.red)
        self.setAcceptHoverEvents(True)


class GraphicView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 800, 1000)

        # self.moveObject = MovingObject(50, 50, 60)
        # self.moveObject2 = MovingObject(100, 100, 100)
        self.stayobject = StaySurface(200,200,500,600)
        for i in range(0,6):
            self.scene.addItem(MovingObject(50, 50, (i+1)*20))
        # self.scene.addItem(self.moveObject2)
        self.scene.addItem(self.stayobject)
