from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from sys import exit


class Tray(QSystemTrayIcon):
    def __init__(self, father):
        super().__init__(father)
        self.father = father

        self.setIcon(QIcon('image/main.ico'))
        self.setToolTip('infinite壁纸')
        self.activated.connect(self.raise_up)

        self.menu = QMenu()
        self.set_action = QAction('设置', self)
        self.set_action.setIcon(QIcon('image/set.ico'))
        self.set_action.triggered.connect(self.set)
        self.exit_action = QAction('退出', self)
        self.exit_action.setIcon(QIcon('image/exit.ico'))
        self.exit_action.triggered.connect(self.exit_)
        self.menu.addActions([self.set_action, self.exit_action])

        self.setContextMenu(self.menu)
        self.show()

    def raise_up(self, e):
        if e == QSystemTrayIcon.Trigger and self.father.config['show_windmill'] != 0:
            self.father.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
            self.father.show()
            self.father.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
            self.father.show()

    def set(self):
        self.raise_up(QSystemTrayIcon.Trigger)
        if self.father.set.isHidden():
            self.father.set.show()

    def exit_(self):
        self.hide()
        self.father.switch_frame.abort = True
        exit()
