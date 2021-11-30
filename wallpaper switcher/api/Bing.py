from requests import get
from re import search, findall
from urllib.request import quote

from . import BaseSpider

class Bing(BaseSpider):
    def __init__(self, father):
        super(Bing, self).__init__(father, self.__class__.__name__)
        self.interval, self.start = 10, 0

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAtUExURQyEhBuMjCiSkjWZmViqqmiysn++vo7GxpzNzarU1MPg4NDo6OLw8PL5+f///0o0y0kAAABJSURBVAhbY2CAAyYDKIPthACU8UYBg6EEY1i2KEAYau+2K0Ck1r1LgCi2gjJM970LADHernu3BKz43btjYF1MOcehJjLDbIUAAEkRGUX4y4rvAAAAAElFTkSuQmCC'
        self.cate = ['随机', 'nature', 'animals', 'landscapes', '自然', '风景', 'mountains', '山水', 'world', '季节', '影视', 'movies', '清新', '护眼', '创意', 'architecture', 'forest']

    def a_page_spider(self, cate):
        return ''.join(get('https://cn.bing.com/images/async?q={0}&first={1}&count={4}&qft=+filterui%3aimagesize-custom_{2}_{3}&mmasync=1'.format(quote(cate), self.father.data['api'][self.name]['cate_page'][cate], *self.father.resolving, self.interval), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall(r'<divclass="imgpt"><aclass="iusc".*?m=.*?murl&quot;:&quot;(.*?)&quot;.*?href=".*?id=(.*?)&', r)
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[1]

    def a_img_spider(self, data):
        img = get(data[0], stream=True, timeout=self.father.config['timeout'], headers=self.headers)
        tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
