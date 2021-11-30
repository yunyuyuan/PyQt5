from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit


class Verify(QDialog):
    exec_signal = pyqtSignal()
    def __init__(self, father):
        super(Verify, self).__init__(father, Qt.WindowCloseButtonHint)
        self.father = father
        self.setWindowTitle('验证')
        self.setWindowIcon(self.father.set.windowIcon())
        self.result = 0

        self.edit = QLineEdit(self)
        self.edit.setStyleSheet('QLineEdit{min-width:0px;font: 15px;}')
        self.submit = QPushButton('提交', self)
        self.submit.setStyleSheet('QPushButton{min-width: 0;}')
        self.submit.clicked.connect(self.verify)
        self.v_label = VLabel(self)

        self.exec_signal.connect(self.exec)

    def verify(self):
        if self.father.api.verify_code(self.edit.text()):
            self.result = 1
            self.close()
        else:
            self.v_label.init()

    def closeEvent(self, e):
        if self.result == 0:
            self.result = -1

    def showEvent(self, e):
        self.result = 0
        self.v_label.init()


class VLabel(QLabel):
    def __init__(self, father):
        super(VLabel, self).__init__('', father)
        self.father, self.top = father, father.father
        self.setToolTip('点击切换验证码')
        self.pix = QPixmap('image/v.png')
        self.set_pix()

    def mousePressEvent(self, e):
        if e.button() == 1:
            self.init()

    def init(self):
        # 下载验证码并显示
        self.top.api.download_code()
        self.pix = QPixmap('image/v.png')
        self.set_pix()

    def set_pix(self):
        # 显示验证码
        self.setGeometry(0, 0, self.pix.width(), self.pix.height())
        self.father.setGeometry(self.top.x()-100, self.top.y()-self.height(), self.width()+100, self.height())
        self.setPixmap(self.pix)
        self.father.edit.setGeometry(self.width(), 10, 60, self.height()-20)
        self.father.edit.clear()
        self.father.submit.setGeometry(self.width()+60, 10, 40, self.height()-20)

    def enterEvent(self, e):
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, e):
        self.setCursor(Qt.ArrowCursor)
