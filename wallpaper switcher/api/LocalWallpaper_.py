from os import listdir
from os.path import join, normcase
from re import search
from tool import set_wall
from random import shuffle


class LocalWallpaper(object):
    def __init__(self, father):
        self.father = father
        self.img_dir, self.img_idx = [], 0

    def init_check(self):
        self.img_dir = []
        try:
            file_list = listdir(self.father.config['directory'])
        except TypeError:
            return
        for f in file_list:
            tail = search(r'.*?\.([a-zA-Z]{3,4})$', f)
            if tail and tail.group(1).lower() in ['jpg', 'png', 'jpeg', 'bmp']:
                self.img_dir.append(normcase(join(self.father.config['directory'], f)))
        if not self.img_dir:
            self.father.config['directory'] = 0
            self.father.dump_data('config')
            for c in self.father.set.play_what.children():
                if c.name == '网络':
                    c.set_active()

    def next_wall(self):
        if self.img_idx >= len(self.img_dir):
            self.img_idx = 0
        if self.img_idx == 0 and self.father.config['random_switch'] != '从不':
            # 从头开始打乱
            shuffle(self.img_dir)
        self.father.switch_frame.white_label.move(0, -50)
        set_wall(self.img_dir[self.img_idx])
        self.img_idx += 1
