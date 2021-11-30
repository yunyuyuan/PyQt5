import PIL.Image as img
import PIL.ImageOps as imp
from PIL.ImageFilter import BoxBlur
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QLabel, QComboBox, QListView, QLineEdit, QMessageBox, QSlider, QDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QColor
from re import search
from numpy import array, sqrt, asarray, gradient, sin, cos, pi
from sys import argv, exit
from os import getcwd
from os.path import getsize
from img_label import ImgLabel


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('图片处理器')
        self.setWindowIcon(QIcon('images/ico.png'))
        self.setGeometry(100, 100, 500, 500)
        self.setFixedSize(930, 650)
        self.file_path = 'images/unknow.jpg'
        self.category = 'jpg'
        self.old_category = 'jpg'
        self.mirror = [1, 1]
        self.default_size = [0, 0]
        self.is_draw = False
        self.pen_bold = 1
        self.color_list = ['#FFFFFF', '#FF0000', '#00FF00', '#000000', "#A52A2A", "#FFD700", "#808080", "#FFA500",
                           "#FFFF00", "#F5DEB3", "#FFC0CB", '#ACFFB8']
        self.warning_count = 0
        # ########################初始化基础控件############################
        # 初始和效果图
        self.choose_img = ImgLabel(self, 1)
        self.result_img = ImgLabel(self, 2)
        self.size_1 = QLabel(self)
        self.size_2 = QLabel(self)
        self.choose_button = QPushButton('选择图片', self)
        self.result_button = QPushButton('展示缩略图', self)
        # 中间的箭头
        self.point_label = QLabel(self)
        # 图片类型
        self.category_choose = QComboBox(self)
        self.category_label = QLabel('转换格式:jpg', self)
        # 大小
        self.size_label = QLabel('转换大小:', self)
        self.size_slider = QSlider(Qt.Horizontal, self)
        self.slider_label = QLabel('缩放:0%', self)
        self.size_width = QLineEdit(self)
        self.size_height = QLineEdit(self)
        # 艺术效果
        self.artistic_choose = QComboBox(self)
        self.artistic_label = QLabel('艺术效果:原始', self)
        # 旋转和镜像
        self.rotate_slider = QSlider(Qt.Horizontal, self)
        self.rotate_label = QLabel('旋转角度:0°', self)
        self.x_mirror = QPushButton('x-镜像', self)
        self.y_mirror = QPushButton('y-镜像', self)
        # 涂鸦
        self.draw_label = QLabel('涂鸦', self)
        self.draw_choose = QComboBox(self)
        self.draw_choose.addItem('不涂鸦')
        self.draw_choose.setStyleSheet('QComboBox{max-width: 50px;}'
                                       'QComboBox::item{max-height:20px;}')
        self.draw_choose.setView(QListView())
        self.pen_slider = QSlider(Qt.Horizontal, self)
        self.pen_label = QLabel('笔尖粗度:1', self)
        for i in self.color_list:
            pix = QPixmap(QSize(130, 22))
            pix.fill(QColor(i))
            self.draw_choose.addItem(QIcon(pix), None)
            self.draw_choose.setIconSize(QSize(130, 22))
            self.draw_choose.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.draw_choose.currentIndexChanged.connect(self.draw)
        # 还原按钮
        self.remove_button = QPushButton('还原涂鸦', self)
        # 保存按钮
        self.save_button = QPushButton('', self)
        # 关于按钮
        self.about_button = QPushButton('', self)

        self.init_widget()

    # 设置基础控件
    def init_widget(self):
        # 展示待处理图片
        self.choose_img.move(10, 10)
        self.result_img.move(510, 10)
        self.size_1.setFixedSize(150, 30)
        self.size_1.move(150, 370)
        self.size_2.setFixedSize(150, 30)
        self.size_2.move(650, 370)
        self.show_img(self.file_path, 1, show_options=True)
        self.set_img()
        # 箭头
        self.point_label.setFixedSize(100, 100)
        self.point_label.move(410, 165)
        self.point_label.setStyleSheet("QLabel{background-image:url(%s);background-repeat:none;}" % 'images/point.png')
        # 选择图片的按钮
        self.choose_button.setFixedSize(80, 30)
        self.choose_button.move(150, 400)
        self.choose_button.clicked.connect(self.get_img)
        # 展示按钮
        self.result_button.setFixedSize(80, 30)
        self.result_button.move(650, 400)
        self.result_button.clicked.connect(self.set_img)
        # ################ 下面的options #############################
        # 类别
        self.category_label.setFixedSize(120, 50)
        self.category_label.move(20, 450)
        self.category_label.setStyleSheet("QLabel{font-size:19px;font-family:kaiti}")
        self.category_choose.move(20, 500)
        self.category_choose.setView(QListView())
        self.category_choose.addItems(['jpg', 'png', 'jpeg', 'gif', 'bmp'])
        self.category_choose.currentIndexChanged.connect(self.change_category)
        # 大小
        self.size_label.setFixedSize(120, 50)
        self.size_label.move(180, 450)
        self.size_label.setStyleSheet("QLabel{font-size:19px;font-family:kaiti}")
        width_label = QLabel('宽:', self)
        height_label = QLabel('高:', self)
        width_label.setStyleSheet('QLabel{max-width:20px;}')
        height_label.setStyleSheet('QLabel{max-width:20px}')
        height_label.move(240, 500)
        width_label.move(160, 500)
        self.size_width.setFixedSize(50, 30)
        self.size_width.move(180, 500)
        self.size_height.setFixedSize(50, 30)
        self.size_height.move(260, 500)
        self.size_slider.setMinimum(-10)
        self.size_slider.setMaximum(10)
        self.size_slider.move(180, 550)
        self.size_slider.valueChanged[int].connect(self.change_size_slider)
        self.slider_label.setFixedSize(150, 20)
        self.slider_label.move(200, 590)
        # 艺术效果
        self.artistic_label.setFixedSize(120, 50)
        self.artistic_label.move(350, 450)
        self.artistic_label.setStyleSheet("QLabel{font-size:19px;font-family:kaiti;min-width:200px}")
        self.artistic_choose.move(350, 500)
        self.artistic_choose.setView(QListView())
        self.artistic_choose.addItems(['原始', '黑白', '反色', '流年', '模糊', '油画', '手绘'])
        self.artistic_choose.currentIndexChanged.connect(self.artistic_button)
        # 旋转和镜像
        self.rotate_slider.setMinimum(0)
        self.rotate_slider.setMaximum(36)
        self.rotate_slider.move(520, 500)
        self.rotate_slider.valueChanged[int].connect(self.change_rotate_slider)
        self.rotate_label.setFixedSize(100, 50)
        self.rotate_label.move(520, 450)
        self.rotate_label.setStyleSheet("QLabel{font-size:19px;font-family:kaiti;min-width:200px}")
        self.x_mirror.move(510, 550)
        self.y_mirror.move(590, 550)
        self.x_mirror.setFixedSize(60, 30)
        self.y_mirror.setFixedSize(60, 30)
        self.x_mirror.clicked.connect(self.change_x)
        self.y_mirror.clicked.connect(self.change_y)
        # 涂鸦
        self.draw_label.setFixedSize(55, 30)
        self.draw_label.move(710, 460)
        self.draw_label.setStyleSheet("QLabel{font-size:19px;font-family:kaiti;}")
        self.draw_choose.move(680, 500)
        self.pen_slider.setMinimum(1)
        self.pen_slider.setMaximum(8)
        self.pen_slider.move(680, 550)
        self.pen_slider.valueChanged[int].connect(self.change_pen)
        self.pen_label.setFixedSize(150, 20)
        self.pen_label.move(700, 590)
        # 保存
        self.save_button.move(845, 565)
        self.save_button.setFixedSize(80, 80)
        self.save_button.setStyleSheet('QPushButton{background-image: url(images/save.png);'
                                        'background-color:transparent;background-repeat:no-repeat;'
                                        'border:none;}'
                                        'QPushButton::hover{background-image: url(images/save_hover.png);}')
        self.save_button.clicked.connect(self.click_save)
        # 还原和关于
        self.remove_button.move(800, 500)
        self.remove_button.clicked.connect(self.remove_pen)
        self.about_button.setFixedSize(57, 51)
        self.about_button.setStyleSheet('QPushButton{background-image: url(images/about_btn.png);'
                                        'background-color:transparent;background-repeat:no-repeat;'
                                        'border:none;}'
                                        'QPushButton::hover{background-image: url(images/about_hover.png);}')
        self.about_button.move(10, 590)
        self.about_button.clicked.connect(self.about)
        # 设置qss样式
        with open('style.qss') as fp:
            qss = fp.read()
        self.setStyleSheet(qss)
        fp.close()

    # ############################## 点击事件 ###########################
    # 点击选择图片
    def get_img(self):
        file = QFileDialog.getOpenFileUrl(self, "选择图片", getcwd(), "Image Files(*.jpg;*.jpeg;*.png;*.gif;*.bmp)")
        if file[1]:
            # 清除涂鸦
            self.result_img.draw_list = []
            self.result_img.all_draw = []
            self.result_img.has_draw = False
            # 路径
            self.file_path = file[0].toString()[8:]
            self.show_img(self.file_path, 1, show_options=True)
            self.set_img()

    # 点击图片类型
    def change_category(self):
        self.category_label.setText('转换格式:'+self.category_choose.currentText())
        self.old_category = self.category
        self.category = self.category_choose.currentText()
        self.warning_count = 0
        self.set_img()

    # 点击缩放
    def change_size_slider(self):
        value = int(self.size_slider.value()*50)
        self.slider_label.setText('缩放:'+str(value)+'%')
        self.size_width.setText(str(self.default_size[0]*(value+500)//500))
        self.size_height.setText(str(self.default_size[1]*(value+500)//500))

    # 点击旋转
    def change_rotate_slider(self):
        value = int(self.rotate_slider.value() * 10)
        self.rotate_label.setText('旋转角度:' + str(value) + '°')
        self.set_img()

    # 点击保存
    def click_save(self):
        self.set_img()
        file_path = search('/([^/]*?)\..*?$', self.file_path).group(1)+'__convert'+'.'+self.category
        image = img.open('images/exhibits/exhibit.'+self.category)
        self.save_img(image, file_path)
        image.close()
        QMessageBox.information(self, '成功！', '保存成功', QMessageBox.Ok, QMessageBox.Ok)

    # 点击艺术效果
    def artistic_button(self):
        self.artistic_label.setText('艺术效果:'+self.artistic_choose.currentText())
        self.set_img()

    # 点击镜像
    def change_x(self):
        self.mirror[0] *= -1
        self.set_img()

    def change_y(self):
        self.mirror[1] *= -1
        self.set_img()

    # 点击绘画颜色
    def draw(self):
        idx = self.draw_choose.currentIndex()
        if idx == 0:
            self.is_draw = False
            self.draw_label.setStyleSheet('QLabel{font-size:19px;font-family:kaiti;}')
            self.result_img.x_move, self.result_img.y_move = 0, 0
        else:
            self.is_draw = self.color_list[idx-1]
            self.draw_label.setStyleSheet('QLabel{border:1px solid%s;font-size:19px;'
                                          'font-family:kaiti;}' % self.color_list[idx-1])

    # 点击笔尖粗细
    def change_pen(self):
        value = int(self.pen_slider.value())
        self.pen_bold = value
        self.pen_label.setText('笔尖粗度:'+str(value))

    # 点击还原涂鸦
    def remove_pen(self):
        self.result_img.draw_list = []
        self.result_img.all_draw = []
        self.result_img.has_draw = False
        self.set_img()

    # 点击关于
    def about(self):
        about_dialog = QDialog()
        about_dialog.setWindowTitle("关于")
        about_dialog.setWindowIcon(QIcon('images/ico.png'))
        about_dialog.setWindowFlags(Qt.WindowCloseButtonHint)
        with open('style.qss') as fp:
            qss = fp.read()
        about_dialog.setStyleSheet(qss)
        about_dialog.setGeometry(350+self.x(), 250+self.y(), 300, 330)
        mine_label = QLabel(about_dialog)
        mine_label.setFixedSize(170, 170)
        mine_label.move(70, 0)
        mine_label.setStyleSheet('QLabel{background-image: url(images/about.png);background-repeat:no-repeat;}')
        close_button = QPushButton('知道了', about_dialog)
        close_button.move(130, 290)
        close_button.clicked.connect(about_dialog.close)
        info_label = QLabel(about_dialog)
        info_label.setFixedSize(250, 170)
        info_label.move(25, 110)
        info_label.setStyleSheet('QLabel{border: 1px solid#FFFFFF}')
        idx = 0
        for info in ['作者:yunyuyuan.', '更新日志:', '    增加旋转镜像功能', '    增加涂鸦功能', '⚠注意:无法修改透明的png图片', '  连续多次修改可能造成内存溢出']:
            label = QLabel(info, info_label)
            label.setStyleSheet('QLabel{border:none;}')
            label.move(10, 10+idx*21)
            idx += 1
        link_label = QLabel(info_label)
        link_label.setOpenExternalLinks(True)
        link_label.setText('🔎详情访问<a href=\"https://github.com/yunyuyuan/invoker/tree/master/pyqt/图片处理\">github地址</a>')
        link_label.setStyleSheet('QLabel{border:none;font-size:18px;font-family:MicrosoftYaHei;}')
        link_label.move(10, 140)
        about_dialog.setWindowModality(Qt.ApplicationModal)
        about_dialog.exec_()

    # ############################## 处理图片 ###########################
    # 改变艺术效果
    def change_artistic(self, image):
        artistic = self.artistic_choose.currentText()
        image = image.convert('RGB')
        if artistic == '黑白':
            image = image.convert('L')
        elif artistic == '流年':
            image = asarray(image.convert('RGB'))
            im1 = sqrt(image * [1.0, 0.0, 0.0]) * 12
            im2 = image * [0.0, 1.0, 1.0]
            image = im1 + im2
            image = img.fromarray(array(image).astype('uint8'))
        elif artistic == '反色':
            image = imp.invert(image)
        elif artistic == '模糊':
            image = image.filter(BoxBlur(20))
        elif artistic == '油画':
            a = asarray(image.convert('L')).astype('float')

        elif artistic == '手绘':
            a = asarray(image.convert('L')).astype('float')
            depth = 10.
            grad = gradient(a)
            grad_x, grad_y = grad
            grad_x = grad_x * depth / 100.
            grad_y = grad_y * depth / 100.
            A = sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
            uni_x = grad_x / A
            uni_y = grad_y / A
            uni_z = 1. / A

            vec_el = pi / 2.2
            vec_az = pi / 4.
            dx = cos(vec_el) * cos(vec_az)
            dy = cos(vec_el) * sin(vec_az)
            dz = sin(vec_el)

            b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)
            b = b.clip(0, 255)

            image = img.fromarray(b.astype('uint8'))
        return image

    # 改变大小
    def change_size(self, image):
        try:
            width = int(self.size_width.text())
            height = int(self.size_height.text())
        except ValueError:
            QMessageBox.warning(self, '警告！', '请输入合法数字', QMessageBox.Ok, QMessageBox.Ok)
            self.size_width.setText(str(self.default_size[0]))
            self.size_height.setText(str(self.default_size[1]))
            self.size_slider.setValue(0)
            return
        if width <= 0 or width >= 8000 or height <= 0 or height >= 8000:
            QMessageBox.warning(self, '警告！', '请输入1-7999的数字', QMessageBox.Ok, QMessageBox.Ok)
            self.size_width.setText(str(self.default_size[0]))
            self.size_height.setText(str(self.default_size[1]))
            self.size_slider.setValue(0)
            return
        return image.resize([width, height])

    # 改变旋转和镜像
    def change_rotate(self, image):
        if self.mirror[0] == -1:
            image = imp.mirror(image)
        if self.mirror[1] == -1:
            image = imp.flip(image)
        rotate_value = self.rotate_slider.value()*10
        if rotate_value:
            image = image.rotate(rotate_value, expand=1)
        return image

    # ########################## 根据options制作图片 ############################
    def make_img(self):
        temporary_img = img.open(self.file_path)
        temporary_img.save('images/exhibits/exhibit.' + self.category)
        # 已经有涂鸦
        if self.result_img.has_draw:
            if self.category == 'gif':
                self.result_img.draw_list = []
                self.result_img.all_draw = []
                self.result_img.has_draw = False
                if self.warning_count == 0:
                    QMessageBox.warning(self, '警告！', 'GIF格式的图片无法涂鸦！', QMessageBox.Ok, QMessageBox.Ok)
                    self.warning_count = 1
            else:
                temporary_img = self.result_img.re_blit()
        # 艺术效果
        temporary_img = self.change_artistic(temporary_img)
        # 大小
        temporary_img = self.change_size(temporary_img)
        if not temporary_img:
            return
        # 旋转镜像
        temporary_img = self.change_rotate(temporary_img)
        return temporary_img

    # 保存图片
    def save_img(self, image, file_path):
        if self.category == 'png':
            image = image.convert('RGBA')
        else:
            image = image.convert('RGB')
        image.save(file_path, quality=100)
        image.close()

    # 显示效果图
    def set_img(self):
        file_path = 'images/exhibits/exhibit.' + self.category
        image = self.make_img()
        if not image:
            return
        self.save_img(image, file_path)
        self.result_img.size_change = 1.0
        self.show_img(file_path, 2)

    # 显示图片
    def show_img(self, file_path, how, show_options=False):
        file_tail = search("\\.(.*)$", file_path).group(1).lower()
        # 打开目标文件并展示缩略图
        temporary_img = img.open(file_path)
        if show_options:
            # 还原options
            self.default_size = list(temporary_img.size)
            self.category_choose.setCurrentText(file_tail)
            self.category = file_tail
            self.size_width.setText(str(temporary_img.size[0]))
            self.size_height.setText(str(temporary_img.size[1]))
            self.size_slider.setValue(0)
            self.slider_label.setText('缩放:0%')
            self.artistic_choose.setCurrentText("原始")
            self.artistic_label.setText('艺术效果:原始')
            self.rotate_slider.setValue(0)
            self.rotate_label.setText('旋转角度:0°')
            self.mirror = [1, 1]
        temporary_img.thumbnail([400, 350])
        if how == 1:
            temporary_img.save('images/temporarys/temporary.%s' % file_tail)
            self.size_1.setText('大小:' + str(round(getsize(file_path) / 1024, 2)) + 'K')
            self.choose_img.img_position = [200 - temporary_img.size[0] // 2, 175 - temporary_img.size[1] // 2]
            self.choose_img.change_img('images/temporarys/temporary.%s' % file_tail, temporary_img.size)
        else:
            temporary_img.save('images/temporarys/temporary_exhibit.%s' % file_tail)
            self.size_2.setText('大小:' + str(round(getsize(file_path) / 1024, 2)) + 'K')
            self.result_img.img_position = [200 - temporary_img.size[0] // 2, 175 - temporary_img.size[1] // 2]
            self.result_img.change_img('images/temporarys/temporary_exhibit.%s' % file_tail, temporary_img.size)
        temporary_img.close()


app = QApplication(argv)
window = Window()
window.show()
exit(app.exec_())

