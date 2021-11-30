from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from json import dump, load
from os import listdir
from os.path import dirname
from re import sub, match, search, findall
from sys import argv

from requests import get, post
from urllib.request import quote
from random import randint, shuffle, choice

from api.LocalWallpaper_ import LocalWallpaper

all_api = ['随机']
for py in listdir('api'):
    if match('.*?[^_]\.py$', py):
        name = sub('\.py', '', py)
        exec('from api.%s import %s' % (name, name))
        all_api.append(name)

from tray import Tray
from frames.switch_frame import SwitchFrame
from frames.set import Set
from frames.right_frame import Right
from frames.choose_random import ChooseRandom
from frames.verify import Verify
from tool import try_author


class Main(QMainWindow):
    def __init__(self):
        super().__init__(None, flags=Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        desktop = QApplication.desktop().screenGeometry()
        self.resolving, self.desktop_resolving = [desktop.width(), desktop.height()], [desktop.width(), desktop.height()]
        self.position = [self.resolving[0] - 150, self.resolving[1] - 150]
        self.size_ = [150, 150]
        self.setGeometry(*self.position, *self.size_)

        self.all_api = all_api
        self.last_api = None
        self.data = {}
        self.config = {}
        self.running_info = {}

        self.initializing = True
        self.base_path = dirname(argv[0])
        self.my_path = argv[0]

        self.init()

    def init(self):
        self.load_data('data')
        self.load_data('config')
        # 初始化分辨率
        if self.config['resolving'] == [0, 0]:
            self.config['resolving'] = self.resolving
            self.dump_data('config')
        else:
            self.resolving = self.config['resolving']
        for api in self.all_api[1:]:
            exec('self.%s = %s(self)' % (api, api))

        self.tray = Tray(self)
        self.switch_frame = SwitchFrame(self)
        self.right_frame = Right(self)
        self.set = Set(self)
        # 检查权限
        if not try_author():
            self.set.auto_start.setEnabled(False)

        self.choose_random = ChooseRandom(self.set, self)
        self.local_api = LocalWallpaper(self)
        self.verify = Verify(self)
        self.local_api.init_check()

        # qss
        with open('style.qss', 'r') as fp:
            self.setStyleSheet(fp.read())

        self.initializing = False
        if self.config['show_windmill'] == 0:
            self.hide()
        else:
            self.show()

    def next_wall(self, err_count=0):
        if self.config['api'] == '随机':
            self.api = eval('self.%s' % choice(list((set(self.all_api[1:]) | set(self.data['ignore_api'])) - (
                    set(self.all_api[1:]) & set(self.data['ignore_api'])))))
        if self.config['play_what'] == '网络':
            self.api.download_img()
        elif self.config['play_what'] == '收藏':
            can = False
            for api in self.all_api[1:]:
                if eval('self.data["api"]["%s"]["like_list"]' % api):
                    can = True
                    break
            if not can:
                self.set.status_label.setText('请至少收藏一张壁纸!')
                self.set.status_timer = 200
                self.config['play_what'] = '网络'
                for c in self.set.play_what.children():
                    if c.name == '网络':
                        c.set_active()
                self.dump_data('config')
                return
            self.api = eval("self.%s" % choice(self.all_api[1:]))
            result = eval("self.api.static_download()")
            if not result and err_count < 5:
                self.next_wall(err_count+1)
        else:
            self.local_api.next_wall()

    def load_data(self, what):
        with open(what + '.json', 'r') as fp:
            exec('self.%s = load(fp)' % what)

    def dump_data(self, what):
        with open(what + '.json', 'w') as fp:
            dump(eval('self.' + what), fp, indent=4)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication(argv)
    main = Main()
    app.exec_()
