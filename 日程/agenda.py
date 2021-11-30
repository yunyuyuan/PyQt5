from PyQt5.QtWidgets import QFrame, QLabel, QPushButton, QTextEdit, QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from json import load


class Agenda(QFrame):
    def __init__(self, father):
        super().__init__(father)
        self.setObjectName('agenda')
        self.father = father
        self.setGeometry(0, 50, self.father.width(), 2400)

        self.color_list = ['#FF3030', '#EEEE00', '#D1EEEE', '#BF3EFF',
                           '#B3EE3A', '#008B8B', '#5CACEE', '#FFB5C5']
        self.pos_y = 50

        self.init()

    def init(self):
        self.arrow_label = QLabel('', self)
        self.arrow_label.setProperty('cate', 'arrow')
        self.arrow_label.setFixedSize(55, 50)

        # 检查是否有保存的
        with open('agenda.json', 'r') as fp:
            data = load(fp)
            fp.close()
        if data:
            for i in range(48):
                exec('self.line_{0} = LineFrame(self, self.father, {0}, space={1})'.format(i, data[i][0]))
                obj = eval('self.line_{0}'.format(i))
                obj.origin_text = data[i][1]
                exec('self.line_{0}.move(0, {1})'.format(i, i*50))
        else:
            for i in range(48):
                exec('self.line_{0} = LineFrame(self, self.father, {0})'.format(i))
                exec('self.line_{0}.move(0, {1})'.format(i, i*50))
        for i in range(48):
            exec('self.line_{0}.init_height()'.format(i))

        self.alter(True)

    def update_line(self, index, hide):
        if hide:
            return eval('self.line_{0}.hide_()'.format(index))
        else:
            exec('self.line_{0}.show_()'.format(index))

    # 滚轮
    def wheelEvent(self, e):
        if self.father.editable:
            orient = e.angleDelta().y()
            if orient > 0:
                if self.pos_y < 50:
                    self.pos_y += 70
                    if self.pos_y > 50:
                        self.pos_y = 50
            else:
                if self.pos_y > self.father.size_[1]-2400:
                    self.pos_y -= 70
                    if self.pos_y < self.father.size_[1]-2400:
                        self.pos_y = self.father.size_[1]-2400
            self.move_()

    def move_(self):
        self.move(0, self.pos_y)
        self.father.head.raise_()

    # 打开/关闭编辑
    def alter(self, do):
        if do:
            self.arrow_label.hide()
        else:
            self.arrow_label.show()
        for i in range(48):
            exec('self.line_{0}.alter({1})'.format(i, do))


class LineFrame(QFrame):
    def __init__(self, father, top, name, space=1, text=''):
        super().__init__(father)
        self.setProperty('cate', 'line_frame')
        self.father, self.top, self.index = father, top, name

        self.width_ = self.top.size_[0]
        self.setObjectName(str(name))
        self.space = 1
        self.origin_text = text
        self.origin_space = space-1
        self.color_index = name % len(self.father.color_list)
        self.hide_list = []

        self.edit_lock = False
        self.init()

    def init(self):
        self.left_frame = QFrame(self)
        left_layout = QVBoxLayout(self.left_frame)
        self.time_label = QLabel('<b>%s:%s0</b>' % (self.index//2, (self.index % 2)*3), self.left_frame)
        self.color_button = QPushButton(' ', self.left_frame)
        self.color_button.setFixedSize(30, 20)
        self.color_button.clicked.connect(self.change_color)
        self.color_button.setProperty('cate', 'palette')
        if (self.index % 2) == 0:
            self.time_label.setProperty('cate', 'hour')
        else:
            self.time_label.setProperty('cate', 'minute')
        self.time_label.setFixedSize(45, 20)
        left_layout.addWidget(self.time_label, alignment=Qt.AlignTop)
        left_layout.addWidget(self.color_button, alignment=Qt.AlignCenter)
        self.left_frame.setLayout(left_layout)
        self.left_frame.move(0, 0)

        self.edit = QTextEdit(self)
        self.edit.selectionChanged.connect(self.align_)
        self.edit.move(60, 0)

        self.right_frame = QFrame(self)
        btn_layout = QVBoxLayout(self.right_frame)
        self.add_button = QPushButton('', self.right_frame)
        self.del_button = QPushButton('', self.right_frame)
        self.add_button.setProperty('cate', 'add')
        self.del_button.setProperty('cate', 'del')
        self.add_button.clicked.connect(lambda: self.add_del('a'))
        self.del_button.clicked.connect(lambda: self.add_del('d'))
        self.add_button.setFixedSize(30, 30)
        self.del_button.setFixedSize(30, 30)
        btn_layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        btn_layout.addWidget(self.del_button, alignment=Qt.AlignCenter)
        self.right_frame.setLayout(btn_layout)
        self.right_frame.move(self.top.size_[0]-60, 0)

        self.refresh()
        self.change_color()

    # 初始化edit内容和行占位
    def init_height(self):
        self.edit.setText(self.origin_text)
        self.edit.setTextColor(QColor(0, 0, 0))
        while self.origin_space > 0:
            self.origin_space -= 1
            self.add_del('a')
        self.edit.setAlignment(Qt.AlignHCenter)

    # 随时改变居中
    def align_(self):
        if not self.edit_lock:
            self.edit_lock = True
            self.edit.setAlignment(Qt.AlignHCenter)
            self.edit_lock = False

    # 打开/关闭编辑
    def alter(self, do, old_space=None):
        if do:
            self.right_frame.show()
            self.edit.verticalScrollBar().show()
            self.color_button.show()
            self.add_button.show()
            self.edit.setEnabled(True)
            width = 0.72
            if self.space > 1:
                self.del_button.show()
            else:
                self.del_button.hide()
        else:
            self.right_frame.hide()
            self.edit.verticalScrollBar().hide()
            self.color_button.hide()
            self.edit.setEnabled(False)
            width = 0.83
        if old_space:
            self.size_animal(self.edit, old_space, self.space, self.top.size_[0] * width, (60, 0), (60, 0))
        else:
            self.edit.setGeometry(60, 0, self.top.size_[0] * width, 50 * self.space)
        self.edit.setAlignment(Qt.AlignHCenter)

    # 增减行占位
    def add_del(self, what):
        old_space = self.space
        if what == 'a' and self.space < 22:
            c = self.father.update_line(self.index+self.space, True)
            self.space += c
        elif what == 'd' and self.space > 1:
            self.space -= 1
            self.father.update_line(self.index+self.space, False)
        self.refresh(old_space=old_space, active=True)

    # 隐藏行
    def hide_(self):
        old_space = self.space
        self.space = 0
        self.refresh(old_space=old_space)
        return old_space

    # 显示行
    def show_(self):
        self.space = 1
        self.refresh(old_space=0, active=True)

    # 更新行大小
    def refresh(self, old_space=None, active=False):
        if not old_space and old_space != 0:
            self.setGeometry(0, self.index * 50, self.width_, self.space * 50)
            self.left_frame.setGeometry(0, 0, 60, self.space * 50)
            self.right_frame.setGeometry(self.width_-60, 0, 60, 50 * self.space)
        else:
            if not active:
                new_y = (self.index + abs(old_space - self.space)) * 50
            elif old_space == 0:
                self.move(0, self.index * 50+50)
                new_y = self.index * 50
            else:
                new_y = self.index * 50
            self.size_animal(self, old_space, self.space, self.width_, [self.pos().x(), self.pos().y()], [0, new_y])
            self.size_animal(self.left_frame, old_space, self.space, 60, (0, 0), (0, 0))
            self.size_animal(self.right_frame, old_space, self.space, 60, (self.width_-60, 0), (self.width_-60, 0))
        self.alter(True, old_space=old_space)

    # 调色板
    def change_color(self):
        self.color_index = (self.color_index + 1) % len(self.father.color_list)
        color = self.father.color_list[self.color_index]
        self.edit.setStyleSheet('QTextEdit{background-color: %s;}' % color)

    # 到点提醒
    def clock(self, time):
        if self.edit.toPlainText():
            self.top.tray.show_a_message(time, self.edit.toPlainText())

    # 动画效果
    def size_animal(self, obj, old_space, new_space, width, old_position, new_position):
        # 动画效果
        animal = QPropertyAnimation(obj, b'geometry', self)
        animal.setDuration(200)
        animal.setStartValue(QRect(*old_position, width, 50 * old_space))
        animal.setEndValue(QRect(*new_position, width, 50 * new_space))
        animal.start()
