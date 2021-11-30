from util import do_from_img, do_from_camera
from PyQt5.Qt import *


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__(None)
        desktop = QApplication.desktop().screen()
        center = (desktop.width() // 2, desktop.height() // 2)
        self.setWindowTitle("二维码识别")
        self.setGeometry(center[0] - 500, center[1] - 300, 1000, 600)

        self.head = Head(self)
        self.body = Body(self)

        self.init()

    def init(self):
        layout = QGridLayout(self)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 4)
        layout.addWidget(self.head, 0, 0)
        layout.addWidget(self.body, 1, 0)
        self.setLayout(layout)
        with open('style.qss') as f:
            self.setStyleSheet(f.read())
        self.show()


class Head(QFrame):
    def __init__(self, father):
        super().__init__(father)
        self.setObjectName('head')
        self.top = father
        layout = QGridLayout(self)
        self.from_img = QPushButton('读取图片', self)
        self.from_img.clicked.connect(self.open_process)
        self.from_cmr = QPushButton('读取摄像头', self)
        self.from_cmr.clicked.connect(self.open_process)
        layout.addWidget(self.from_img, 0, 0)
        layout.addWidget(self.from_cmr, 0, 1)
        self.setLayout(layout)

    def open_process(self):
        if self.sender().text() == '读取图片':
            self.top.body.read_from_img()
        else:
            self.top.body.read_from_cmr()


class Body(QFrame):
    def __init__(self, father):
        super().__init__(father)
        self.setObjectName('body')
        self.top = father
        layout = QGridLayout(self)
        self.img = ImgLabel(self)
        self.img.hide()
        self.result = QFrame(self)
        layout1 = QGridLayout(self.result)
        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(0)
        self.result.setLayout(layout1)
        self.result.hide()
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 1)
        layout.addWidget(self.img, 0, 0)
        layout.addWidget(self.result, 0, 1)
        self.setLayout(layout)

        self.scroll_f = None
        self.labels_frame = None

    def read_from_cmr(self):
        re = do_from_camera()
        self.go_result(re)

    def read_from_img(self):
        re = do_from_img()
        self.go_result(re)

    def go_result(self, re):
        if re:
            self.img.show()
            arr = re[0]
            info = re[1]
            self.img.put_pix(QPixmap(QImage(arr, arr.shape[1], arr.shape[0], 3 * arr.shape[1], QImage.Format_RGB888)))
            if self.scroll_f is not None:
                self.scroll_f.deleteLater()
            layout = self.result.layout()
            self.scroll_f = QScrollArea()
            self.labels_frame = LabelsFrame(self.result, info)
            self.scroll_f.setWidget(self.labels_frame)
            layout.addWidget(self.scroll_f)
            self.result.show()

    def resizeEvent(self, e):
        if self.labels_frame is not None:
            self.labels_frame.setFixedWidth(self.scroll_f.width()-20)

class ImgLabel(QLabel):
    def __init__(self, father):
        super().__init__(father)
        self.top = father
        self.pix = None

    def put_pix(self, pix):
        self.pix = pix
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        i_size = [self.pix.width(), self.pix.height()]
        s_size = [self.width(), self.height()]
        scale = min(s_size[0] / i_size[0], s_size[1] / i_size[1])
        new_size = list(map(lambda s: s * scale, i_size))
        p.drawPixmap(QRect(abs(s_size[0] - new_size[0]) // 2, abs(s_size[1] - new_size[1]) // 2, int(new_size[0]),
                           int(new_size[1])), self.pix, QRect(0, 0, int(i_size[0]), int(i_size[1])))
        super(ImgLabel, self).paintEvent(e)

class LabelsFrame(QFrame):
    def __init__(self, father, info):
        super().__init__(father)
        self.father = father

        layout = QVBoxLayout(self)
        for i in range(len(info)):
            label = QTextEdit(f'<b style="color:red">{i + 1}.</b>{info[i]}', self)
            label.adjustSize()
            layout.addWidget(label)
        self.setLayout(layout)

if __name__ == '__main__':
    from sys import argv

    app = QApplication(argv)
    main = Main()
    app.exec_()
