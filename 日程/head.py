from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from time import strftime, localtime
from json import dump


class Head(QFrame):
    def __init__(self, father):
        super().__init__(father)
        self.setObjectName('head')
        self.father = father
        self.setGeometry(0, 0, self.father.size_[0], 50)

        self.setMouseTracking(True)
        self.init()

    def init(self):
        self.raise_()
        self.time_label = QLabel(strftime("%Y-%m-%d %H:%M:%S", localtime()), self)
        self.locate_button = DragButton(self, self.father)
        self.finish_button = QPushButton('', self)
        self.locate_button.setObjectName('locate')
        self.finish_button.setObjectName('finish')
        self.finish_button.clicked.connect(self.finish)

        horizon = QHBoxLayout(self)
        horizon.setContentsMargins(0, 0, 0, 0)
        horizon.addWidget(self.finish_button, alignment=Qt.AlignLeft)
        horizon.addWidget(self.time_label, alignment=Qt.AlignCenter)
        horizon.addWidget(self.locate_button, alignment=Qt.AlignRight)
        self.setLayout(horizon)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    # 一秒更新一次时间
    def update_time(self):
        time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.time_label.setText(time)
        if time[-2:] == '00':
            self.locate()

    # 打开/关闭编辑
    def alter(self, do):
        if do:
            self.locate_button.show()
            self.finish_button.show()
        else:
            self.locate_button.hide()
            self.finish_button.hide()

    # 关闭编辑
    def finish(self):
        self.father.editable = False
        self.locate()
        self.alter(False)
        self.father.agenda.alter(False)
        # 保存
        with open('agenda.json', 'w') as fp:
            write_data = []
            for i in range(48):
                obj = eval('self.father.agenda.line_{0}'.format(i))
                write_data.append([obj.space, obj.edit.toPlainText()])
            dump(write_data, fp, indent=4)
            fp.close()

    # 一分钟更新一次定位
    def locate(self):
        if not self.father.editable:
            time_percent = int(strftime("%H", localtime()))*100 + int(strftime("%M", localtime()))*5//3
            self.father.agenda.pos_y = (self.father.size_[1])/5 - time_percent + 25
            if self.father.agenda.pos_y > 50:
                self.father.agenda.pos_y = 50
            elif self.father.agenda.pos_y < self.father.size_[1]-2400:
                self.father.agenda.pos_y = self.father.size_[1]-2400
            self.father.agenda.move_()
            self.father.agenda.arrow_label.move(50, time_percent-24)
            self.father.agenda.arrow_label.raise_()
            # 提示
            for i in range(48):
                obj = eval('self.father.agenda.line_{0}'.format(i))
                pos_y = obj.pos().y()
                is_hide = obj.isHidden()
                if pos_y == time_percent and not is_hide:
                    obj.clock(strftime("%H:%M", localtime()))
                    break


class DragButton(QPushButton):
    def __init__(self, father, top):
        super().__init__('', father)
        self.father = father
        self.top = top

        self.hand = False
        self.move_x = 0

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.hand = True
            e.accept()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, e):
        self.hand = False
        self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, e):
        if self.hand:
            if self.top.move_x == 0:
                self.move_x = e.x()
            if 0 < self.top.move_x + (e.x() - self.move_x) < 1920-self.top.size_[0]:
                self.top.move_x += (e.x() - self.move_x)
                self.top.move(self.top.move_x, 0)
                self.top.set.data['move_x'] = self.top.move_x
