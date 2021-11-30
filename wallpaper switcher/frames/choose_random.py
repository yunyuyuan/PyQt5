from math import ceil
from PyQt5.QtWidgets import QDialog, QFrame, QGridLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt
from sip import delete


class ChooseRandom(QDialog):
    def __init__(self, father, top):
        super().__init__(father, Qt.WindowCloseButtonHint)
        self.father, self.top = father, top
        self.setWindowTitle('随机选项')
        self.setObjectName('choose_random')
        self.move(self.father.x()+self.father.width()//2-200, self.father.y()+self.father.height()//2-150)

        self.list = LeftFrame(self, top)
        self.list_scroll = ScrollFrame(self, self.list, 140)

        self.color_frame = QFrame(self)
        self.color_frame.setObjectName('choose_mid')
        self.color_frame.move(155, 0)

        self.tags = RightFrame(self, top)
        self.tags.move(186, 0)
        self.tags_scroll = ScrollFrame(self, self.tags, 165)

        self.resize(500, 300)
        self.setMinimumSize(500, 300)

    def showEvent(self, e):
        self.move(self.father.x()+self.father.width()//2-self.width()//2, self.father.y()+self.father.height()//2-self.height()//2)

    def resizeEvent(self, e):
        self.list.resize(self.list.width(), self.height())

        self.color_frame.resize(3, self.height())

        self.tags.resize(self.width() - 190, self.height())

        for w in [self.list_scroll, self.tags_scroll]:
            w.resize(8, self.height())

    def resize_(self):
        self.tags.resize_()
        for w in [self.list_scroll, self.tags_scroll]:
            w.resize_()


class LeftFrame(QFrame):
    def __init__(self, father, top):
        super().__init__(father)
        self.setObjectName('api_frame')
        self.father, self.top = father, top
        self.setGeometry(0, 0, 150, 300)

        self.all_api = self.top.all_api[1:]
        self.now_api = self.all_api[0]

        self.inside_frame = QFrame(self)
        self.inside_frame.resize(self.width(), len(self.all_api)*55+5)
        self.inside_frame.move(0, 0)
        self.inside_frame.setObjectName('inside')

        for idx in range(len(self.all_api)):
            label = ApiLabel(self.all_api[idx], self, self.top)
            label.move(7, idx*55+5)

    def wheelEvent(self, e):
        if self.inside_frame.height() > self.height():
            if e.angleDelta().y() > 0:
                self.inside_frame.move(0, self.inside_frame.y() + 60)
                if self.inside_frame.y() > 0:
                    self.inside_frame.move(0, 0)
            else:
                self.inside_frame.move(0, self.inside_frame.y() - 60)
                if self.inside_frame.y() < self.height()-self.inside_frame.height():
                    self.inside_frame.move(0, self.height()-self.inside_frame.height())
            self.father.list_scroll.bar.setValue(abs(self.inside_frame.y()))


class ApiLabel(QLabel):
    def __init__(self, name, father, top):
        super().__init__(name, father.inside_frame)
        self.father, self.top, self.name = father, top, name

        self.setProperty('cate', 'api_label')
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, e):
        if e.button() == 1:
            self.father.now_api = self.name
            for c in self.father.inside_frame.children():
                c.change_style()
            self.top.choose_random.tags.init()
            self.top.choose_random.resize_()
        elif e.button() == 2:
            if self.text() in self.top.data['ignore_api']:
                self.top.data['ignore_api'].remove(self.text())
            else:
                self.top.data['ignore_api'].append(self.text())
            self.top.dump_data('data')
            self.change_style()

    def showEvent(self, e):
        self.change_style()

    def change_style(self):
        if self.text() not in self.top.data['ignore_api']:
            if self.text() == self.father.now_api:
                color = "pink"
            else:
                color = "#52AAED"
        else:
            color = 'gray'
        self.setStyleSheet("""
                        QLabel{
                            border-radius: 4px;
                            border: 1px solid;
                            background: %s;
                            font: 15px;
                        }
                        QLabel:hover{
                            border: 1px solid red;
                            color: red;
                        }""" % color)
        self.setFixedSize(120, 50)


class RightFrame(QFrame):
    def __init__(self, father, top):
        super().__init__(father)
        self.setObjectName('tag_frame')
        self.father, self.top = father, top
        self.resize(322, 300)

        self.inside_frame = QFrame(self)
        self.inside_frame.setObjectName('right_inside')
        self.inside_frame.move(0, 0)

        self.now_api = None
        self.init()

    def init(self):
        self.now_api = eval('self.top.%s' % self.father.list.now_api)
        for c in self.inside_frame.children():
            delete(c)
        self.inside_frame.resize(self.width(), ceil(len(self.now_api.cate[1:])/((self.width())//95))*45+5)
        self.inside_frame.move(0, 0)
        for idx in range(len(self.now_api.cate[1:])):
            label = TagLabel(self.now_api.cate[1:][idx], self, self.top)
            label.setToolTip(label.text())
            label.move(4+95*(idx % (self.width()//95)), (idx//(self.width()//95)) * 45+5)

    def wheelEvent(self, e):
        if self.inside_frame.height() > self.height():
            if e.angleDelta().y() > 0:
                self.inside_frame.move(0, self.inside_frame.y() + 60)
                if self.inside_frame.y() > 0:
                    self.inside_frame.move(0, 0)
            else:
                self.inside_frame.move(0, self.inside_frame.y() - 60)
                if self.inside_frame.y() < self.height() - self.inside_frame.height():
                    self.inside_frame.move(0, self.height() - self.inside_frame.height())
            self.father.tags_scroll.bar.setValue(abs(self.inside_frame.y()))

    def resizeEvent(self, e):
        self.resize_()

    def resize_(self):
        self.inside_frame.move(0, 0)
        self.inside_frame.resize(self.width(), ceil(len(self.now_api.cate[1:])/((self.width())//95))*45+5)
        self.father.tags_scroll.mid_frame.setGeometry(0, 0, 0, self.inside_frame.height())
        a_line = self.width() // 95
        for c in range(len(self.inside_frame.children())):
            self.inside_frame.children()[c].move(4+95*(c % a_line)+(self.width()-a_line*95)*(c % a_line)/a_line, 45*(c // a_line)+5)


class TagLabel(QLabel):
    def __init__(self, name, father, top):
        super().__init__(name, father.inside_frame)
        self.father, self.top, self.name = father, top, name
        self.setProperty('cate', 'tag_label')
        self.setAlignment(Qt.AlignCenter)
        self.show()
        self.setFixedSize(90, 40)

    def mousePressEvent(self, e):
        if e.button() == 1:
            if self.name in eval('self.top.data["api"]["%s"]["ignore_list"]' % self.top.choose_random.list.now_api):
                eval('self.top.data["api"]["%s"]["ignore_list"]' % self.top.choose_random.list.now_api).remove(self.name)
            else:
                eval('self.top.data["api"]["%s"]["ignore_list"]' % self.top.choose_random.list.now_api).append(self.name)
            # 检查是否已全不在
            if len(eval('self.top.data["api"]["%s"]["ignore_list"]' % self.top.choose_random.list.now_api)) == len(self.father.now_api.cate[1:]) and self.top.choose_random.list.now_api not in self.top.data['ignore_api']:
                self.top.data['ignore_api'].append(self.top.choose_random.list.now_api)
                for c in self.top.choose_random.list.inside_frame.children():
                    c.change_style()
            elif self.top.choose_random.list.now_api in self.top.data['ignore_api']:
                self.top.data['ignore_api'].remove(self.top.choose_random.list.now_api)
                for c in self.top.choose_random.list.inside_frame.children():
                    c.change_style()
            self.top.dump_data('data')
            for c in self.father.inside_frame.children():
                c.change_style()

    def showEvent(self, e):
        self.change_style()

    def change_style(self):
        if self.text() in eval('self.top.data["api"]["%s"]["ignore_list"]' % self.top.choose_random.list.now_api):
            color = "gray"
        else:
            color = "#99EDA5"
        self.setStyleSheet("""
            QLabel{
                border-radius: 4px;
                border: 1px solid;
                background: %s;
                font: 13px;
            }
            QLabel:hover{
                border: 1px solid red;
                color: red;
        }""" % color)
        self.setFixedSize(90, 40)


class ScrollFrame(QFrame):
    def __init__(self, father, parent, pos_x):
        super().__init__(father)
        self.parent_, self.father, self.pox_x = parent, father, pos_x
        self.setStyleSheet('QFrame{background: transparent;}')

        self.mid_frame = MidFrame(self)
        self.mid_frame.setGeometry(0, 0, 0, self.parent_.inside_frame.height())

        self.scroll = QScrollArea()
        self.bar = self.scroll.verticalScrollBar()
        self.scroll.setWidget(self.mid_frame)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        layout = QGridLayout(self)
        layout.addWidget(self.scroll, 0, 0)
        self.setLayout(layout)

        self.setGeometry(pos_x, 0, 8, self.father.height())

    def resizeEvent(self, e):
        self.resize_()

    def resize_(self):
        self.scroll.setGeometry(0, 0, 8, self.height())


class MidFrame(QFrame):
    def __init__(self, father):
        super().__init__(father)
        self.father = father

    def moveEvent(self, e):
        self.father.parent_.inside_frame.move(self.father.parent_.inside_frame.x(), e.pos().y())
