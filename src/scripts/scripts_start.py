import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from src.scripts import  bommerger
class ScriptsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Объединитель Excel")
        self.setGeometry(860, 450, 300, 200)

        self.button_merge = QPushButton("Объединитель Excel(xlsx,xls,xlsm)", self)
        self.button_merge.setGeometry(50, 30, 200, 40)

        self.button_back = QPushButton("Назад", self)
        self.button_back.setGeometry(50, 130, 200, 40)


        self.button_merge.clicked.connect(self.merge_excel)
        self.button_back.clicked.connect(self.home_window)

    def merge_excel(self):
        '''открытие окна Объединитель excel'''
        self.merge_window = bommerger.Bommerger()
        self.close()
        self.merge_window.show()


    def home_window(self):
        '''открытие окна дом'''
        self.home_window = backend_auth.AuthWindow()
        self.close()
        self.home_window.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScriptsMainWindow()
    window.show()
    sys.exit(app.exec_())

