from os.path import join
from os import remove
from shutil import copyfile

from PyQt5.QtWidgets import QFrame, QLabel, QMenu, QAction
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtCore import Qt, QTimer, QEvent, QPoint, pyqtSignal
from threading import Thread
from tool import set_wall


class SwitchFrame(QFrame):
    process_signal = pyqtSignal(int)
    def __init__(self, father):
        super().__init__(father)
        self.father = father
        self.abort = False

        self.setGeometry(0, 0, 75, 100)

        self.color_frame = QFrame(self)
        self.color_frame.setObjectName('color_frame')
        self.color_frame.setGeometry(34, 38, 9, 62)

        self.white_label = QLabel('', self.color_frame)
        self.white_label.setObjectName('white_label')
        self.white_label.setGeometry(0, 0, 9, 62)
        self.process_signal.connect(lambda x:self.white_label.move(0, x))

        self.windmill_label = WindMill(self, self.father)

        self.timer = QTimer()
        self.interval = 13
        self.timer.setInterval(self.interval)
        self.timer.start()
        self.timer.timeout.connect(self.rotate)

        self.switch_timer = QTimer()
        self.switch_timer.start(1000)
        self.switch_timer.timeout.connect(self.auto_switch)

        self.step_time = 0

    def rotate(self):
        if self.windmill_label.add == 0:
            return
        elif self.windmill_label.add == 1:
            if self.interval > 3.2:
                self.interval -= 0.1
                self.timer.setInterval(self.interval)
        else:
            if self.interval < 12.8:
                self.interval += 0.1
                self.timer.setInterval(self.interval)
            else:
                self.windmill_label.add = 0
        self.windmill_label.angle = (self.windmill_label.angle - 1) % 360
        self.windmill_label.update()

    def auto_switch(self):
        if self.father.config['switch'] != 0:
            self.step_time += 1
            if self.step_time == self.father.config['switch']:
                self.windmill_label.switch(type_=True)
                self.step_time = 0


class WindMill(QLabel):
    set_ = pyqtSignal()
    def __init__(self, father, top):
        super().__init__('', father)
        self.set_.connect(set_wall)
        self.father, self.top = father, top
        self.setGeometry(0, 0, 75, 75)
        self.pix = QPixmap('image/windmill.png')
        self.setToolTip('来点好玩的')

        self.handle = False
        self.pressed = False
        self.move_pos = QPoint(0, 0)

        self.add = 0
        self.angle = 0

        self.downloading = False

        self.menu = QMenu(self)
        self.set_action = self.top.tray.set_action
        self.exit_action = self.top.tray.exit_action
        self.download_action = QAction(QIcon('image/download.png'), '下载', self)
        self.download_action.triggered.connect(self.download)
        self.menu.addActions([self.set_action, self.download_action, self.exit_action])

    def paintEvent(self, p):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(37.5, 38)
        painter.rotate(self.angle)
        painter.translate(-37.5, -38)
        painter.drawPixmap(12, 13, 50, 50, self.pix)

    def event(self, e):
        # 鼠标移进移出
        if e.type() == QEvent.Enter:
            self.setCursor(Qt.PointingHandCursor)
            self.top.right_frame.scale_state = 1
        elif e.type() == QEvent.Leave:
            self.setCursor(Qt.ArrowCursor)
            if self.top.right_frame.like_label.width() == 40:
                self.top.right_frame.scale_delay = 50
            self.top.right_frame.scale_state = -1

        return super().event(e)

    def contextMenuEvent(self, e):
        self.menu.exec_(self.mapToGlobal(e.pos()))

    def mousePressEvent(self, e):
        self.pressed = True
        self.move_pos = e.pos()

    def mouseReleaseEvent(self, e):
        self.pressed = False
        if self.handle:
            self.handle = False
        else:
            if e.button() == 1:
                self.switch()

    def switch(self, type_=False):
        if not self.downloading:
            self.father.abort = False
            self.add = 1
            self.downloading = True
            self.setToolTip('点击取消')
            self.top.set.api_choose.setEnabled(False)
            self.top.set.category_choose.setEnabled(False)
            Thread(target=self.process_download).start()
        elif not self.father.abort and not type_:
            # 停止
            self.father.abort = True

    def mouseMoveEvent(self, e):
        if self.pressed:
            self.handle = True
            self.top.position = [self.top.position[0] + e.x() - self.move_pos.x(), self.top.position[1] + e.y() - self.move_pos.y()]
            self.top.setGeometry(*self.top.position, *self.top.size_)

    def process_download(self):
        # 开始下载
        try:
            self.top.next_wall()
        except:
            # 无论什么错误都忽略
            pass
        # 下载完毕
        self.downloading = False
        self.setToolTip('来点好玩的')
        self.add = -1
        self.father.step_time = 0

        if self.top.config['play_what'] == '网络':
            self.top.set.api_choose.setEnabled(True)
            self.top.set.category_choose.setEnabled(True)
        if not self.father.abort and self.top.config['play_what'] != '本地':
            self.set_.emit()
        self.father.abort = False
        self.father.process_signal.emit(0)
        self.top.right_frame.reload_pix()
        if self.top.api.name+'_'+str(self.top.api.current_id) in self.top.data['download_list']:
            self.download_action.setIcon(QIcon('image/cancel_download.png'))
            self.download_action.setText('删除')
        else:
            self.download_action.setIcon(QIcon('image/download.png'))
            self.download_action.setText('下载')

    def download(self):
        try:
            if self.top.api.current_id and self.top.config['directory'] != 0:
                if self.download_action.text() == '下载':
                    copyfile('image/wall.jpg', join(self.top.config['directory'], self.top.api.name+'_'+str(self.top.api.current_id)+'.jpg'))
                    self.top.data['download_list'].append(self.top.api.name+'_'+str(self.top.api.current_id))
                    self.top.dump_data('data')
                    self.download_action.setIcon(QIcon('image/cancel_download.png'))
                    self.download_action.setText('删除')
                else:
                    remove(join(self.top.config['directory'], self.top.api.name + '_' + str(self.top.api.current_id) + '.jpg'))
                    self.top.data['download_list'].remove(self.top.api.name+'_' + str(self.top.api.current_id))
                    self.top.dump_data('data')
                    self.download_action.setIcon(QIcon('image/download.png'))
                    self.download_action.setText('下载')
        except:
            return
