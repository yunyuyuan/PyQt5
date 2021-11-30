from PyQt5.QtWidgets import QDialog, QComboBox, QSlider, QListView, QCheckBox, QFrame, QGridLayout, QLabel, QPushButton, \
    QFileDialog, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont
from PyQt5.QtCore import Qt, QEvent, QTimer, QByteArray, QSize
from tool import auto_start, dump_log
from webbrowser import open_new_tab
from requests import get
from re import search, findall, sub
from threading import Thread, Lock


lock = Lock()
class Set(QDialog):
    def __init__(self, father):
        super().__init__(father, Qt.WindowCloseButtonHint)
        self.father = father

        self.setObjectName('set')
        self.setWindowTitle('设置')
        self.setWindowIcon(QIcon('image/set.ico'))
        self.move_pos = [self.father.desktop_resolving[0]//2-300, self.father.desktop_resolving[1]//2-200]
        self.size_ = [600, 400]
        self.setGeometry(*self.move_pos, *self.size_)

        combobox_frame = QFrame(self)
        api_label = QLabel('接口', combobox_frame)
        api_label.setProperty('cate', 'combo_label')
        api_label.setAlignment(Qt.AlignCenter)
        self.api_choose = QComboBox(self)
        self.api_choose.setToolTip('选择寻找壁纸的网站')
        self.api_choose.currentTextChanged.connect(lambda: self.set_change('api'))
        api_list_view = QListView()
        api_list_view.entered.connect(self.show_name)
        self.api_choose.setView(api_list_view)

        category_label = QLabel('分类', combobox_frame)
        category_label.setProperty('cate', 'combo_label')
        category_label.setAlignment(Qt.AlignCenter)
        self.category_choose = QComboBox(self)
        self.category_choose.setToolTip('选择壁纸类型')
        self.category_choose.currentTextChanged.connect(lambda: self.set_change('cate'))
        category_list_view = QListView()
        category_list_view.entered.connect(self.show_name)
        self.category_choose.setView(category_list_view)

        grid_1 = QGridLayout()
        grid_1.setContentsMargins(0, 30, 0, 30)
        grid_1.setSpacing(0)
        grid_1.addWidget(api_label, 0, 0, 1, 1)
        grid_1.addWidget(category_label, 0, 1, 1, 1)
        grid_1.addWidget(self.api_choose, 1, 0, 1, 1)
        grid_1.addWidget(self.category_choose, 1, 1, 1, 1)
        combobox_frame.setLayout(grid_1)

        remain_frame = QFrame(self)

        switch_label = QLabel('自动切换', remain_frame)
        switch_label.setProperty('cate', 'indicate_label')
        self.switch_list = ["从不", "30秒", "1分钟", "5分钟", "10分钟", "30分钟", "1小时", "2小时", "5小时", "10小时"]
        self.true_switch_list = [0, 30, 60, 300, 600, 1800, 3600, 7200, 18000, 36000]
        self.switch_slider = QSlider(Qt.Horizontal, self)
        self.switch_slider.setToolTip('自动切换壁纸')
        self.switch_slider.setMaximum(9)
        self.switch_slider.setValue(self.true_switch_list.index(self.father.config['switch']))
        self.switch_slider.valueChanged.connect(lambda: self.set_change('switch'))
        self.switch_show = QLabel(self.switch_list[self.true_switch_list.index(self.father.config['switch'])], remain_frame)

        size_label = QLabel('大小限制', remain_frame)
        size_label.setProperty('cate', 'indicate_label')
        self.size_list = ["不限制", "500K", "1M", "2M", "5M", "10M", "20M"]
        self.true_size_list = [0, 500, 1000, 2000, 5000, 10000, 20000]
        self.size_slider = QSlider(Qt.Horizontal, self)
        self.size_slider.setToolTip('限制图片大小')
        self.size_slider.setMaximum(6)
        self.size_slider.setValue(self.true_size_list.index(self.father.config['length']))
        self.size_slider.valueChanged.connect(lambda: self.set_change('size'))
        self.size_show = QLabel(self.size_list[self.true_size_list.index(self.father.config['length'])], remain_frame)

        self.show_windmill = QCheckBox('桌面显示风车', self)
        self.show_windmill.setToolTip('桌面显示切换风车')
        self.show_windmill.setCheckState(self.father.config['show_windmill'])
        self.show_windmill.stateChanged.connect(lambda: self.set_change('show_windmill'))

        random_switch_frame = QFrame(self)
        random_switch_label = QLabel('随机切换', random_switch_frame)
        random_switch_label.setAlignment(Qt.AlignCenter)
        random_switch_label.setProperty('cate', 'head_label')
        self.random_switch = PartFrame(self, self.father, 'random_switch', random_switch_frame)
        self.random_switch.setToolTip('随机切换壁纸')
        self.random_switch.set_part([['从不', '顺序切换', 'border-right: 1px solid;border-top-left-radius: 10px;border-top-right-radius: 0;border-bottom-right-radius: 0;border-bottom-left-radius: 10px;'],
                                     ['一类', '每一次切换都是随机分类(仅分类选项为随机时可用)', 'border-right: 1px solid;border-radius: 0;'],
                                     ['一页', '每一页的壁纸顺序都被打乱', 'border: 0px solid;border-top-left-radius: 0;border-top-right-radius: 10px;border-bottom-right-radius: 10px;border-bottom-left-radius: 0;']])
        random_switch_frame.setFixedSize(122, 57)
        self.random_switch.move(0, 25)

        play_what_frame = QFrame(self)
        play_what_label = QLabel('选壁纸源', play_what_frame)
        play_what_label.setAlignment(Qt.AlignCenter)
        play_what_label.setProperty('cate', 'head_label')
        self.play_what = PartFrame(self, self.father, 'play_what', play_what_frame)
        self.play_what.setToolTip('选择壁纸源')
        self.play_what.set_part([['网络', '网络壁纸', 'border-right: 1px solid;border-top-left-radius: 10px;border-top-right-radius: 0;border-bottom-right-radius: 0;border-bottom-left-radius: 10px;'],
                                     ['收藏', '已收藏的壁纸', 'border-right: 1px solid;border-radius: 0;'],
                                     ['本地', '本地壁纸(右键选择文件夹)', 'border-left: 0px solid;border-top-left-radius: 0;border-top-right-radius: 10px;border-bottom-right-radius: 10px;border-bottom-left-radius: 0;']])
        play_what_frame.setFixedSize(122, 57)
        self.play_what.move(0, 25)

        self.auto_start = QCheckBox('开机自动启动', self)
        self.auto_start.setToolTip('设置软件开机自启')
        self.auto_start.setCheckState(self.father.config['auto_start'])
        self.auto_start.stateChanged.connect(lambda: self.set_change('auto_start'))

        grid_2 = QGridLayout()
        grid_2.addWidget(switch_label, 0, 0, 1, 1)
        grid_2.addWidget(size_label, 1, 0, 1, 1)
        grid_2.addWidget(self.switch_slider, 0, 1, 1, 2)
        grid_2.addWidget(self.size_slider, 1, 1, 1, 2)
        grid_2.addWidget(self.switch_show, 0, 3, 1, 1)
        grid_2.addWidget(self.size_show, 1, 3, 1, 1)

        grid_2.addWidget(self.show_windmill, 2, 0, 1, 2)
        grid_2.addWidget(self.auto_start, 2, 2, 1, 2)
        grid_2.addWidget(random_switch_frame, 3, 0, 1, 2)
        grid_2.addWidget(play_what_frame, 3, 2, 1, 2)
        remain_frame.setLayout(grid_2)

        right_frame = QFrame(self)

        self.logo_label = AnimalLabel(self, self.father)
        self.logo_label.setToolTip('随机选项')
        self.logo_label.setObjectName('logo')

        resolution_label = QLabel('分辨率', right_frame)
        resolution_label.setStyleSheet('QLabel{max-width: 1000px;}')
        resolution_label.setAlignment(Qt.AlignCenter)
        resolution_label.setToolTip('依据这个最小分辨率筛选')
        self.width_edit = QLineEdit(str(self.father.config['resolving'][0]), right_frame)
        self.width_edit.setMaxLength(5)
        self.width_edit.setAlignment(Qt.AlignCenter)
        self.width_edit.editingFinished.connect(self.submit_resolution)
        self.height_edit = QLineEdit(str(self.father.config['resolving'][1]), right_frame)
        self.height_edit.setMaxLength(5)
        self.height_edit.setAlignment(Qt.AlignCenter)
        self.height_edit.editingFinished.connect(self.submit_resolution)
        resolution_mid = QLabel('x', right_frame)
        resolution_mid.setStyleSheet('QLabel{max-width: 1000px;}')
        resolution_mid.setAlignment(Qt.AlignCenter)

        clear_button = QPushButton('清空黑名单', right_frame)
        clear_button.setToolTip('清空不喜欢的图片')
        clear_button.clicked.connect(self.clear_list)
        self.update_button = QPushButton('更新接口', right_frame)
        self.update_button.setToolTip('更新可用网站')
        self.update_button.clicked.connect(self.check_update)

        # 状态文字
        self.status_label = QLabel('', self)
        self.status_timer = 0
        self.status_label.setFont(QFont('微软雅黑', 14, QFont.Bold))
        self.status_label.setStyleSheet('QLabel{max-width: 200px;min-width: 200px;color: #A55;}')
        # GitHub
        git_btn = GitLabel(self)

        grid_3 = QGridLayout()
        grid_3.setRowStretch(3, 2)
        grid_3.addWidget(self.logo_label, 0, 2, 1, 6)
        grid_3.addWidget(resolution_label, 1, 0, 2, 2)
        grid_3.addWidget(self.width_edit, 1, 2, 2, 2)
        grid_3.addWidget(resolution_mid,1, 4, 2, 1)
        grid_3.addWidget(self.height_edit, 1, 5, 2, 2)
        grid_3.addWidget(clear_button, 3, 2, 2, 3)
        grid_3.addWidget(self.update_button, 3, 5, 2, 3)
        grid_3.addWidget(self.status_label, 5, 0, 1, 6)
        grid_3.addWidget(git_btn, 5, 6, 1, 1)
        grid_3.setAlignment(Qt.AlignCenter)
        right_frame.setLayout(grid_3)

        mid_label_0 = QLabel('', self)
        mid_label_0.setStyleSheet('QLabel{background: qlineargradient(x1: 0, y1: 0,x2: 1,y2: 0, stop: 0 #FF0000, stop: 1 #0000FF);;max-height: 3px;min-height: 3px;max-width: 10000px;}')
        mid_label_1 = QLabel('', self)
        mid_label_1.setStyleSheet('QLabel{background: qlineargradient(x1: 0, y1: 0,x2: 0,y2: 1, stop: 0 #F0F, stop: 1 #FAA);;max-width: 3px;min-width: 3px;max-height: 10000px;}')

        main_grid = QGridLayout()
        main_grid.setColumnStretch(0, 1)
        main_grid.setColumnStretch(1, 1)
        main_grid.setColumnStretch(2, 1)
        main_grid.setContentsMargins(0, 0, 0, 0)
        main_grid.setSpacing(0)

        main_grid.addWidget(combobox_frame, 0, 0, 1, 1)
        main_grid.addWidget(mid_label_0, 1, 0, 1, 1)
        main_grid.addWidget(remain_frame, 2, 0, 2, 1)
        main_grid.addWidget(mid_label_1, 0, 1, 4, 1)
        main_grid.addWidget(right_frame, 0, 2, 4, 1)
        self.setLayout(main_grid)

        self.timer = QTimer()
        self.interval = 13
        self.timer.setInterval(self.interval)
        self.timer.start()
        self.timer.timeout.connect(self.rotate)

        self.remain_cate_random = False
        self.load_api()

    def load_api(self):
        for api in self.father.all_api:
            pix = QPixmap()
            if api == '随机':
                pix.loadFromData(QByteArray.fromBase64(b'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'))
            else:
                pix.loadFromData(QByteArray.fromBase64(eval('self.father.%s.b64_data' % api)))
            ico = QIcon(pix)
            ico.actualSize(QSize(22, 22))
            self.api_choose.addItem(ico, api)
        self.api_choose.setCurrentText(self.father.config['api'])

        if self.father.config['api'] != '随机':
            self.father.api = eval('self.father.%s' % self.father.config['api'])
            self.category_choose.addItems(self.father.api.cate)
            self.category_choose.setCurrentText(self.father.config['category'])
            if self.father.config['play_what'] != '网络':
                self.api_choose.setEnabled(False)
                self.category_choose.setEnabled(False)
        else:
            self.category_choose.addItem('随机')
            self.category_choose.setCurrentText('随机')

    def rotate(self):
        if self.status_timer > 0:
            self.status_timer -= 1
        elif not self.status_label.isHidden() and self.status_timer != -1:
            self.status_label.setText('')
        if self.logo_label.add == 0:
            return
        elif self.logo_label.add == 1:
            if self.interval > 2.5:
                self.interval -= 0.5
                self.timer.setInterval(self.interval)
        else:
            if self.interval < 15.5:
                self.interval += 0.5
                self.timer.setInterval(self.interval)
            else:
                self.logo_label.add = 0
        self.logo_label.angle = (self.logo_label.angle - 1) % 360
        self.logo_label.update()

    def set_change(self, what):
        if not self.father.initializing:
            if what == 'api':
                self.father.config['api'] = self.api_choose.currentText()
                if self.api_choose.currentText() != '随机':
                    # 保持一类随机
                    if self.father.config['random_switch'] == '一类':
                        self.remain_cate_random = True
                    else:
                        self.remain_cate_random = False
                    # 选择新api
                    exec('self.father.api = self.father.' + self.api_choose.currentText())
                    self.category_choose.clear()
                    self.category_choose.addItems(self.father.api.cate)
                else:
                    self.category_choose.clear()
                    self.category_choose.addItem('随机')
                    self.category_choose.setCurrentText('随机')
            elif what == 'cate':
                self.father.config['category'] = self.category_choose.currentText()
                if self.category_choose.currentText() != '随机' and self.father.config['random_switch'] == '一类' and not self.remain_cate_random:
                    self.father.config['random_switch'] = '一页'
                    for c in self.random_switch.children():
                        if c.name == '一页':
                            c.set_active()
                try:
                    # 选择新的分类
                    self.father.api.img_set, self.father.api.img_idx = [], 0
                except:pass
            elif what == 'switch':
                value = self.switch_slider.value()
                self.switch_show.setText(self.switch_list[value])
                self.father.config['switch'] = self.true_switch_list[value]
                self.father.switch_frame.step_time = 0
            elif what == 'size':
                value = self.size_slider.value()
                self.size_show.setText(self.size_list[value])
                self.father.config['length'] = self.true_size_list[value]
            elif what == 'show_windmill':
                self.father.config['show_windmill'] = self.show_windmill.checkState()
                if self.show_windmill.checkState() == 0:
                    self.father.hide()
                else:
                    self.father.show()
            elif what == 'auto_start':
                if auto_start(int(self.auto_start.checkState()), self.father.my_path):
                    self.father.config['auto_start'] = self.auto_start.checkState()

            self.father.dump_data('config')

    def clear_list(self):
        for api in self.father.data['api']:
            self.father.data['api'][api]['hate_list'] = []
        self.father.dump_data('data')
        self.status_label.setText('清理完成')
        self.status_timer = 200

    def check_update(self):
        self.status_label.setText('检查中...')
        self.status_timer = -1
        self.update_button.setEnabled(False)
        Thread(target=self.check_update_main).start()

    def check_update_main(self):
        try:
            r = ''.join(get('https://github.com/yunyuyuan/invoker/tree/master/pyqt/wallpaper%20switcher/api').content.decode().split())
            api_list = findall(r'<aclass="js-navigation-open"title="(.*?)\.py"', r)
        except:
            dump_log('检查更新'+'--->'+':失败')
            self.status_label.setText('检查失败')
            self.status_timer = 200
            return
        self.not_download = []
        for new in api_list:
            if new not in self.father.all_api and new not in ['__init__', 'LocalWallpaper_']:
                self.not_download.append(new)
        # 下载
        if self.not_download:
            self.status_label.setText('%s个更新,下载中-0个' % str(len(self.not_download)))
            self.status_timer = -1
            for api in self.not_download:
                Thread(target=self.download_api, args=(api, )).start()
        else:
            self.status_label.setText('暂无更新')
            self.status_timer = 200
            self.update_button.setEnabled(True)

    def download_api(self, api, err_count=0):
        r = get('https://raw.githubusercontent.com/yunyuyuan/invoker/master/pyqt/wallpaper%%20switcher/api/%s.py' % api)
        if r.ok:
            with open('api/%s.py' % api, 'wb') as fp:
                fp.write(r.content)
                fp.close()
                self.father.data['api'][api] = {}
                self.father.data['api'][api]['ignore_list'] = []
                self.father.data['api'][api]['like_list'] = []
                self.father.data['api'][api]['hate_list'] = []
                self.father.dump_data('data')
                lock.acquire()
                num = int(search('下载中.(\d*)个', self.status_label.text()).group(1)) + 1
                self.status_label.setText('%s个更新,下载中-%s个' % (str(len(self.not_download)), num))
                self.status_timer = -1
                if num == len(self.not_download):
                    self.status_label.setText('下载完成,重启软件生效')
                    self.status_timer = 200
                    self.update_button.setEnabled(True)
                lock.release()
        elif err_count < 5:
            dump_log('更新api'+'--->'+':出错')
            self.download_api(api, err_count+1)

    def submit_resolution(self):
        try:
            w, h = int(self.width_edit.text()), int(self.height_edit.text())
            if 100 <= w <= 10000 and 100 <= h <= 10000:
                self.father.resolving = [w, h]
                self.father.config['resolving'] = self.father.resolving
                self.father.dump_data('config')
                self.status_label.setText('更新成功!')
                self.status_timer = 200
            else:raise ValueError
        except ValueError:
            self.status_label.setText('请输入3-5位数字!')
            self.status_timer = 200

    # 显示选择的api和分类
    def show_name(self, idx):
        self.status_label.setText(idx.data())
        self.status_timer = 200


class AnimalLabel(QLabel):
    def __init__(self, father, top):
        super().__init__('', father)
        self.father, self.top = father, top
        self.pix = QPixmap('image/windmill.png')
        self.add = 0
        self.angle = 0

    def paintEvent(self, p):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(106, 106)
        painter.rotate(self.angle)
        painter.translate(-106, -106)
        painter.drawPixmap(30, 31, 150, 150, self.pix)

    def event(self, e):
        # 鼠标移进移出
        if e.type() == QEvent.Enter:
            self.setCursor(Qt.PointingHandCursor)
            self.add = 1
        elif e.type() == QEvent.Leave:
            self.setCursor(Qt.ArrowCursor)
            self.add = -1
        return super().event(e)

    def mousePressEvent(self, e):
        if e.button() == 1:
            self.top.choose_random.exec()


class PartFrame(QFrame):
    def __init__(self, father, top, what, parent):
        super().__init__(parent)
        self.father, self.top, self.what = father, top, what
        self.setFixedSize(122, 32)
        self.setStyleSheet("""
            QFrame{
                border-radius: 10px;
                border: 1px solid qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                                                    stop: 0 red, stop: 1 blue);
            }
        """)

    def set_part(self, info):
        idx = 0
        part_length = (self.width()-2)//len(info)
        for part in info:
            f = OnePart(*part, self, self.top, [idx*part_length+1, 1, part_length, self.height()-2])
            if part[0] == self.top.config[self.what]:
                f.set_active()
            idx += 1


class OnePart(QFrame):
    def __init__(self, name, tooltip, style, father, top, g):
        super().__init__(father)
        self.father, self.top, self.name = father, top, name
        self.style_ = """
            QFrame{
                border: none;
                background: #99EDA5;
                %s
            }
        """ % style

        self.setGeometry(*g)
        self.setToolTip(tooltip)
        self.setStyleSheet(self.style_)

        self.label = QLabel(name, self)
        self.label.move(0, 0)
        self.label.setFixedSize(self.width(), self.height())
        self.label.setStyleSheet('QLabel{font: 14px;}')
        self.label.setAlignment(Qt.AlignCenter)

    def event(self, e):
        if e.type() == QEvent.Enter:
            self.setCursor(Qt.PointingHandCursor)
        elif e.type() == QEvent.Leave:
            self.setCursor(Qt.ArrowCursor)
        return super().event(e)

    def mousePressEvent(self, e):
        if e.button() == 1:
            if self.name == '网络' and not self.top.switch_frame.windmill_label.downloading:
                self.top.set.api_choose.setEnabled(True)
                self.top.set.category_choose.setEnabled(True)
            elif self.name == '收藏':
                can = False
                for api in self.top.all_api[1:]:
                    if eval('self.top.data["api"]["%s"]["like_list"]' % api):
                        can = True
                        break
                if not can:
                    self.top.set.status_label.setText('请至少收藏一张壁纸!')
                    self.top.set.status_timer = 200
                    return
                else:
                    self.top.set.api_choose.setEnabled(False)
                    self.top.set.category_choose.setEnabled(False)
            elif self.name == '本地':
                if self.top.config['directory'] == 0:
                    self.top.set.status_label.setText('请先右键选择一个文件夹!')
                    self.top.set.status_timer = 200
                    return
                else:
                    self.top.local_api.init_check()
                    if not self.top.local_api.img_dir:
                        return
                self.top.set.api_choose.setEnabled(False)
                self.top.set.category_choose.setEnabled(False)
            elif self.name == '一类':
                if self.top.config['category'] != '随机':
                    self.top.set.status_label.setText('请先选择随机分类!')
                    self.top.set.status_timer = 200
                    return
                else:
                    for api in self.top.all_api[1:]:
                        eval('self.top.%s' % api).img_set, eval('self.top.%s' % api).img_idx = [], 0
            self.set_active()
            self.top.config[self.father.what] = self.name
            self.top.dump_data('config')
        elif e.button() == 2 and self.name == '本地':
            path = QFileDialog.getExistingDirectoryUrl(self.top.set, "选择文件夹")
            if not path.isEmpty():
                self.top.config['directory'] = sub('file:///', '', path.toString())
                self.top.dump_data('config')


    def set_active(self):
        for c in self.father.children():
            if c is self:
                c.setStyleSheet(sub('background:.*?;', 'background: pink;', c.style_))
            else:
                c.setStyleSheet(sub('background:.*?;', 'background: #99EDA5;', c.style_))


class GitLabel(QLabel):
    def __init__(self, father):
        super().__init__('', father)
        self.father = father
        self.setFixedSize(40, 40)
        self.pix = QPixmap('image/git_btn')

    def mousePressEvent(self, e):
        if e.button() == 1:
            open_new_tab('https://github.com/yunyuyuan/invoker/tree/master/pyqt/wallpaper%20switcher')

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.translate(0, 0)
        painter.drawPixmap(0, 0, 40, 40,self.pix)
        super().paintEvent(e)

    def event(self, e):
        if e.type() == QEvent.Enter:
            self.pix = QPixmap('image/git_hover')
            self.update()
        elif e.type() == QEvent.Leave:
            self.pix = QPixmap('image/git_btn')
            self.update()
        return super().event(e)

    def enterEvent(self, e):
        self.father.status_label.setText('GitHub地址')
        self.father.status_timer = 200
