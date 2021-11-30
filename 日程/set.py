from PyQt5.QtWidgets import QLabel, QPushButton, QSlider, QDialog, QMessageBox, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
# from webbrowser import open_new as web_open
from json import load, dump
from requests import get
from threading import Thread


class Set(QDialog):
    def __init__(self, father):
        super().__init__(father, flags=Qt.WindowCloseButtonHint)
        self.father = father
        self.setWindowTitle('设置')
        self.setObjectName('set')
        self.setWindowIcon(QIcon('images/set.ico'))
        self.setFixedSize(200, 110)

        self.data = {}
        self.init()

    def init(self):
        self.opacity_label = QLabel('透明度 ', self)
        self.opacity_label.move(30, 30)
        self.opacity_label.setFixedSize(80, 20)
        self.height_label = QLabel('高度 ', self)
        self.height_label.move(35, 70)
        self.height_label.setFixedSize(90, 20)

        self.opacity_slider = QSlider(Qt.Horizontal, self)
        self.opacity_slider.setFixedSize(100, 20)
        self.opacity_slider.setMinimum(1)
        self.opacity_slider.setMaximum(10)
        self.opacity_slider.move(10, 10)
        self.opacity_slider.valueChanged[int].connect(self.change_opacity)

        self.height_slider = QSlider(Qt.Horizontal, self)
        self.height_slider.setFixedSize(100, 20)
        self.height_slider.setMinimum(150)
        self.height_slider.setMaximum(900)
        self.height_slider.move(10, 50)
        self.height_slider.valueChanged[int].connect(self.change_height)

        self.save_button = QPushButton('保存', self)
        self.save_button.clicked.connect(self.save_json)
        self.save_button.move(140, 15)

        # self.about_button = QPushButton('关于', self)
        # self.about_button.clicked.connect(lambda: web_open('https://github.com/yunyuyuan/invoker/tree/master/pyqt/日程'))
        # self.about_button.move(130, 55)

        self.update_button = QPushButton('检查更新', self)
        self.update_button.clicked.connect(self.check_update)
        self.update_button.move(130, 55)
        self.update_button.setFixedSize(55, 25)

        self.status_label = QLabel('', self)
        self.status_label.move(120, 85)
        self.status_label.setObjectName('status')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.hide()

        self.progress_bar = QProgressBar(self)
        self.progress_bar.move(120, 85)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()

        self.load_json()
        self.set_data()

    def check_update(self):
        self.new_ver = 0.0
        if self.update_button.text() == '检查更新':
            self.progress_bar.hide()
            self.update_button.setText('检查中...')
            self.update_button.setEnabled(False)

            def download_ver():
                res = get('https://raw.githubusercontent.com/yunyuyuan/invoker/master/pyqt/%E6%97%A5%E7%A8%8B/ver.txt', timeout=5)
                self.update_button.setEnabled(True)
                if res.ok:
                    ver = res.content.decode('utf-8')
                    if float(ver) > self.data['ver']:
                        self.new_ver = float(ver)
                        self.status_label.setText('新版本%s' % ver)
                        self.update_button.setText('在线更新')
                    else:
                        self.update_button.setText('检查更新')
                        self.update_button.setText('暂无更新')
                else:
                    self.status_label.setText('检查失败')
                self.status_label.show()

            Thread(target=download_ver).start()
        elif self.update_button.text() == '在线更新':
            self.update_button.setEnabled(False)
            self.update_button.setText('更新中...')
            self.status_label.hide()
            self.progress_bar.show()

            r = get('https://raw.githubusercontent.com/yunyuyuan/invoker/master/pyqt/%E6%97%A5%E7%A8%8B/update.zip', stream=True)
            length = int(r.headers['Content-Length'])//100
            rate = 0
            with open('update.zip', 'wb') as fp:
                for part in r.iter_content(length):
                    fp.write(part)
                    rate = rate+1 if rate < 100 else 100
                    self.progress_bar.setValue(rate)
                fp.close()
                self.data['ver'] = self.new_ver
                self.save_json()
                self.progress_bar.setValue(0)
                self.progress_bar.hide()
                self.status_label.setText('请重启软件')
                self.status_label.show()
                self.update_button.setText('下载完成')

    def change_opacity(self):
        self.father.setWindowOpacity(int(self.opacity_slider.value())/10)
        self.opacity_label.setText('透明度 ' + str(int(self.opacity_slider.value())/10))

    def change_height(self):
        self.father.size_ = [self.father.size_[0], int(self.height_slider.value())]
        self.father.setFixedSize(*self.father.size_)

        self.height_label.setText('高度 ' + str(self.height_slider.value()))
        self.father.head.locate()

    def load_json(self):
        with open('data.json', 'r') as fp:
            data = load(fp)
            fp.close()
        self.data = data

    def save_json(self):
        with open('data.json', 'w') as fp:
            self.data['opacity'] = int(self.opacity_slider.value())/10
            self.data['height'] = int(self.height_slider.value())
            self.data['move_x'] = int(self.father.move_x)
            dump(self.data, fp)
            fp.close()
            QMessageBox.information(self, '成功', '保存完成', QMessageBox.Ok, QMessageBox.Ok)

    # 更新设置
    def set_data(self):
        self.father.setWindowOpacity(self.data['opacity'])
        self.opacity_label.setText('透明度 ' + str(self.data['opacity']))
        self.opacity_slider.setValue(self.data['opacity']*10)

        self.father.size_ = [self.father.size_[0], self.data['height']]
        self.father.setFixedSize(*self.father.size_)
        self.height_label.setText('高度 ' + str(self.data['height']))
        self.height_slider.setValue(self.data['height'])

        self.father.move_x = self.data['move_x']
        self.father.setGeometry(self.father.move_x, 0, *self.father.size_)

    def closeEvent(self, e):
        self.set_data()
        self.close()
