from PIL.Image import new as new_im
from PIL.ImageDraw import ImageDraw
from PIL.ImageQt import toqpixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


def color_pix(color):
    im = new_im('RGB', (128, 128))
    draw = ImageDraw(im, 'RGB')
    draw.rectangle((0, 0, 128, 128), fill=(int(color[1:3], 16), int(color[3:5], 16), int(color[5:], 16)))
    return toqpixmap(im)

class ResizeLabel(QLabel):
    def __init__(self, f, left_e, right_e):
        super(ResizeLabel, self).__init__(f)
        self.f = f
        self.left, self.right = left_e, right_e
        self.setFixedWidth(5)
        self.setCursor(Qt.SizeHorCursor)
        self.attach = False
        self.start_x = 0

    def mousePressEvent(self, e):
        self.attach = True
        self.start_x = e.globalX()

    def mouseReleaseEvent(self, e):
        self.attach = False

    def mouseMoveEvent(self, e):
        if self.attach:
            delta = e.globalX() - self.start_x
            if (self.f.all_text[self.left].width() + delta) > 50 and (self.f.all_text[self.right].width() - delta) > 50:
                self.f.layout().setColumnStretch(self.left, self.f.all_text[self.left].width() + delta)
                self.f.layout().setColumnStretch(self.right, self.f.all_text[self.right].width() - delta)
            self.start_x = e.globalX()
