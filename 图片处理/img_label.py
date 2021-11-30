from PyQt5.QtWidgets import QLabel, QMessageBox
import PIL.Image as img
from re import search
from PyQt5.QtCore import Qt


class ImgLabel(QLabel):
    def __init__(self, parent, how):
        super().__init__(parent)
        self.setStyleSheet("QLabel{border:1px solid#FFFFFF}")
        self.setFixedSize(400, 350)
        self.how = how
        self.father = parent
        self.size_change = 1.0
        self.mouse_down = False
        self.x_move = 0
        self.y_move = 0
        self.img_size = [0, 0]
        self.default_size = []
        self.img_position = [0, 0]
        self.file_path = None
        mid_label = QLabel(self)
        mid_label.setFixedSize(398, 348)
        mid_label.move(1, 1)
        self.img_label = QLabel(mid_label)
        self.draw_list = []
        self.all_draw = []
        self.has_draw = False

    # 更改背景图片
    def change_img(self, file_path=None, size=None, draw=None):
        if size:
            self.img_size = list(size)
            self.img_label.setFixedSize(*size)
        if file_path:
            self.file_path = file_path
        self.img_label.move(self.img_position[0], self.img_position[1])
        if draw:
            if draw not in self.all_draw:
                self.all_draw.append([draw, self.father.is_draw, self.father.pen_bold])
            if draw not in self.draw_list:
                self.draw_list.append([draw, self.father.is_draw, self.father.pen_bold])
                # 画的超过100个点就显示
                if len(self.draw_list) > 200:
                    self.blit()
        self.img_label.setStyleSheet("QLabel{background-image:url(%s);background-repeat:no-repeat;"
                                     "background-position:center;border:none;}" % self.file_path)

    # 鼠标滚轮事件
    def wheelEvent(self, e):
        if e.angleDelta().y() < 0 and self.size_change > 1.0:
            self.size_change -= 0.1
        elif e.angleDelta().y() > 0 and self.size_change < 3.0:
            self.size_change += 0.1
        if self.how == 1:
            image = img.open(self.father.file_path)
            image.thumbnail([400*self.size_change, 350*self.size_change])
            save_path = 'images/temporarys/temporary.'+search("\\.(.*)$", self.father.file_path).group(1).lower()
        else:
            image = img.open('images/exhibits/exhibit.'+self.father.category)
            image.thumbnail([400 * self.size_change, 350 * self.size_change])
            save_path = 'images/temporarys/temporary_exhibit.' + self.father.category
        size = image.size
        image.save(save_path)
        image.close()
        self.img_position = [(self.img_position[0]-e.x())*size[0]//self.img_size[0]+e.x(),
                             (self.img_position[1] - e.y()) * size[1] // self.img_size[1] + e.y()]
        self.change_img(save_path, size)

    # 画线
    def blit(self):
        self.has_draw = True
        image = img.open('images/exhibits/exhibit.' + self.father.category)
        for pos in self.draw_list:
            for x in range(-pos[2], pos[2]+1):
                for y in range(-pos[2], pos[2]+1):
                    image.putpixel((pos[0][0] + x, pos[0][1] + y), (int(pos[1][1:3], 16), int(pos[1][3:5], 16), int(pos[1][5:], 16)))
        image.save('images/exhibits/exhibit.' + self.father.category)
        image.thumbnail([400 * self.size_change, 350 * self.size_change])
        image.save('images/temporarys/temporary_exhibit.' + self.father.category)
        image.close()
        self.change_img()
        # 重置draw_list
        self.draw_list = []

    def re_blit(self):
        image = img.open('images/exhibits/exhibit.' + self.father.category)
        for pos in self.all_draw:
            for x in range(-pos[2], pos[2]+1):
                for y in range(-pos[2], pos[2]+1):
                    image.putpixel((pos[0][0] + x, pos[0][1] + y), (int(pos[1][1:3], 16), int(pos[1][3:5], 16), int(pos[1][5:], 16)))
        return image

    # 鼠标按住和释放
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # 更新原图大小
            image = img.open('images/exhibits/exhibit.'+self.father.category)
            self.default_size = image.size
            image.close()
            if not self.father.is_draw or self.how == 1:
                self.setCursor(Qt.ClosedHandCursor)
            self.mouse_down = True
            self.x_move = e.x()
            self.y_move = e.y()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.how == 2 and self.draw_list:
                self.blit()
            self.setCursor(Qt.ArrowCursor)
            self.mouse_down = False

    def mouseMoveEvent(self, e):
        if self.mouse_down:
            # 涂鸦
            if self.father.is_draw and self.how == 2:
                if self.father.category == 'gif':
                    QMessageBox.warning(self.father, '警告！', 'GIF格式的图片无法涂鸦！', QMessageBox.Ok, QMessageBox.Ok)
                elif min(400, self.img_position[0]+self.img_size[0]-2) >= e.x() >= max(self.img_position[0]+2, 0) and \
                        min(350, self.img_position[1] + self.img_size[1]-2) >= e.y() >= max(self.img_position[1]+2, 0):
                    self.change_img(draw=[(e.x()-self.img_position[0])*self.default_size[0]//self.img_size[0],
                                          (e.y() - self.img_position[1]) * self.default_size[1] // self.img_size[1]])
            else:
                # 拖动图片
                if 400 >= self.img_position[0] + (e.x()-self.x_move) >= -self.img_size[0]:
                    self.img_position[0] += (e.x() - self.x_move)
                if 350 >= self.img_position[1] + (e.y() - self.y_move) >= -self.img_size[1]:
                    self.img_position[1] += (e.y() - self.y_move)
                self.change_img()
                self.x_move = e.x()
                self.y_move = e.y()

