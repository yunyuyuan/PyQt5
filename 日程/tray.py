from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QDialog, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from sys import exit
from json import dump, load


class Tray(QSystemTrayIcon):
    """ 系统托盘 """
    def __init__(self, father):
        super().__init__(father)
        self.setObjectName('tray')
        self.father = father

        self.init()
        self.show()

    def init(self):
        self.setIcon(QIcon('images/main.ico'))
        self.setToolTip('待办')
        self.activated[QSystemTrayIcon.ActivationReason].connect(self.temporary_raise)

        self.menu = QMenu()
        self.edit_act = QAction('编辑', self)
        self.set_act = QAction('设置', self)
        self.clear_act = QAction('清空', self)
        self.exit_act = QAction('退出', self)
        self.edit_act.setIcon(QIcon('images/edit.ico'))
        self.set_act.setIcon(QIcon('images/set.ico'))
        self.clear_act.setIcon(QIcon('images/clear.ico'))
        self.exit_act.setIcon(QIcon('images/exit.ico'))

        self.menu.addActions([self.edit_act, self.set_act, self.clear_act, self.exit_act])

        self.edit_act.triggered.connect(self.edit_)
        self.exit_act.triggered.connect(self.quit)
        self.clear_act.triggered.connect(self.clear)
        self.set_act.triggered.connect(self.open_set)

        # 右键菜单
        self.setContextMenu(self.menu)

    # 窗口置顶
    def temporary_raise(self, btn):
        if btn == QSystemTrayIcon.Trigger:
            self.father.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
            self.father.show()
            self.father.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
            self.father.show()

    # 打开编辑
    def edit_(self):
        self.temporary_raise(QSystemTrayIcon.Trigger)
        self.father.editable = True
        self.father.head.alter(True)
        self.father.agenda.alter(True)

    # 清空
    def clear(self):
        for i in range(48):
            obj = eval('self.father.agenda.line_{0}'.format(i))
            obj.edit.clear()
            obj.space = 1
            obj.refresh()

    # 退出弹窗
    def quit(self):
        ExitDialog(self, self.father)

    # 打开设置
    def open_set(self):
        rec = [self.geometry().x(), self.geometry().y()]
        self.father.set.move(rec[0]-200, rec[1]-200)
        self.father.set.exec_()

    # 显示一条提示
    def show_a_message(self, t, s):
        self.showMessage(t, s, self.icon())


class ExitDialog(QDialog):
    def __init__(self, father, top):
        super().__init__(top, flags=Qt.WindowCloseButtonHint)
        self.father, self.top = father, top
        self.setWindowIcon(QIcon('images/exit.ico'))
        self.setWindowTitle('退出')
        self.setGeometry(father.geometry().x()-250, father.geometry().y()-120, 250, 120)

        self.warning_label = QLabel('是否保存该日程?', self)
        self.warning_label.setStyleSheet('QLabel{font-size: 18px;}')
        self.warning_pic = QLabel('', self)
        self.warning_pic.setStyleSheet('QLabel{background-image: url(images/quit.png)}')
        self.warning_pic.setFixedSize(61, 74)
        self.warning_label.move(95, 20)
        self.warning_pic.move(10, 20)

        self.yes_btn = QPushButton('保存', self)
        self.cancel_btn = QPushButton('放弃', self)
        self.yes_btn.move(100, 70)
        self.cancel_btn.move(180, 70)

        self.yes_btn.clicked.connect(self.yes)
        self.cancel_btn.clicked.connect(self.cancel)

        self.exec_()

    def yes(self):
        # 保存
        with open('agenda.json', 'w') as fp:
            write_data = []
            for i in range(48):
                obj = eval('self.top.agenda.line_{0}'.format(i))
                write_data.append([obj.space, obj.edit.toPlainText()])
            dump(write_data, fp, indent=4)
            fp.close()
        self.final_do()

    def cancel(self):
        # 不保存
        with open('agenda.json', 'w') as fp:
            dump([], fp)
            fp.close()
        self.final_do()

    def final_do(self):
        with open('data.json', 'r+') as fp:
            data = load(fp)
            data['move_x'] = self.top.move_x
            fp.seek(0)
            dump(data, fp)
            fp.close()
        self.father.hide()
        exit()

