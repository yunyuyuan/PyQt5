from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
from sys import argv

from tray import Tray
from agenda import Agenda
from head import Head
from set import Set


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.setObjectName('main')
        self.setWindowTitle('日程')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowOpacity(1.0)
        self.size_ = [400, 500]
        self.move_x = 1200
        self.setGeometry(self.move_x, 0, *self.size_)

        # 是否可编辑
        self.editable = True

        self.init()
        self.show()

    def init(self):
        self.tray = Tray(self)
        self.head = Head(self)
        self.agenda = Agenda(self)
        self.set = Set(self)
        # qss
        with open('style.QSS', 'r') as fp:
            self.setStyleSheet(fp.read())
            fp.close()


app = QApplication(argv)
window = MainWindow()
app.exec_()
