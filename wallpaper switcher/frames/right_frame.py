from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import QTimer, QEvent, Qt


class Right(QFrame):
    def __init__(self, father):
        super().__init__(father)
        self.father = father
        self.setObjectName('right')
        self.setGeometry(75, 0, 50, 100)

        self.like_label = AnimalLabel(self, father, 'like', [25, 25])
        self.hate_label = AnimalLabel(self, father, 'hate', [25, 75])
        self.scale_state = 0
        self.scale_delay = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.scale)
        self.timer.start(15)
        self.show()

    def scale(self):
        if self.scale_state == 0:
            return
        for w in [self.like_label, self.hate_label]:
            if self.scale_delay > 0:
                self.scale_delay -= 1
                return
            new_size = [w.width()+self.scale_state*5, w.height()+self.scale_state*5]
            if 0 <= new_size[0] <= 40:
                w.setGeometry(w.center_pos[0]-new_size[0]/2, w.center_pos[1]-new_size[1]/2, new_size[0], new_size[1])
                w.update()
            else:
                self.scale_state = 0

    def reload_pix(self):
        if self.father.api.current_id:
            id_, data = self.father.api.current_id, self.father.api.current_data
            if [id_, data] in self.father.data["api"][self.father.last_api]["like_list"]:
                self.like_label.pix = QPixmap('image/liked.png')
                self.like_label.setToolTip('取消收藏')
            else:
                self.like_label.pix = QPixmap('image/like.png')
                self.like_label.setToolTip('加入收藏')

            if id_ in self.father.data["api"][self.father.last_api]["hate_list"]:
                self.hate_label.pix = QPixmap('image/hated.png')
                self.hate_label.setToolTip('取消黑名单')

            else:
                self.hate_label.setToolTip('加入黑名单')
                self.hate_label.pix = QPixmap('image/hate.png')
            self.like_label.update()
            self.hate_label.update()


class AnimalLabel(QLabel):
    def __init__(self, father, top, cate, center_pos):
        super().__init__('', father)
        self.father, self.top = father, top
        if cate == 'like':
            self.setToolTip('加入收藏')
            self.cate, self.another_cate = cate, 'hate'
        else:
            self.setToolTip('加入黑名单')
            self.cate, self.another_cate = cate, 'like'
        self.center_pos = center_pos
        self.setGeometry(*self.center_pos, 0, 0)

        self.pix = QPixmap('image/'+cate+'.png')

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, self.width(), self.height(), self.pix)

    def event(self, e):
        if e.type() == QEvent.Enter:
            if self.width() == 40:
                self.setGeometry(self.x()-5, self.y()-5, 50, 50)
                self.update()
            self.setCursor(Qt.PointingHandCursor)
            self.father.scale_state = 1
        elif e.type() == QEvent.Leave:
            if self.width() == 50:
                self.setGeometry(self.x()+5, self.y()+5, 40, 40)
                self.update()
            self.father.scale_delay = 50
            self.father.scale_state = -1
        return super().event(e)

    def mousePressEvent(self, e):
        if e.button() == 1:
            if self.top.api.current_id:
                id_, data = str(self.top.api.current_id), self.top.api.current_data
                if self.cate == 'like':
                    our, other = [id_, data], id_
                else:
                    other, our = [id_, data], id_
                if our in self.top.data["api"][self.top.last_api][self.cate+"_list"]:
                    # 已存在则删除
                    self.top.data["api"][self.top.last_api][self.cate+"_list"].remove(our)
                else:
                    # 添加
                    self.top.data["api"][self.top.last_api][self.cate+"_list"].append(our)
                    # 删除相反的
                    if other in self.top.data["api"][self.top.last_api][self.another_cate + "_list"]:
                        self.top.data["api"][self.top.last_api][self.another_cate + "_list"].remove(other)
                self.top.dump_data('data')
                # 重新加载pix
                self.father.reload_pix()
                self.update()

