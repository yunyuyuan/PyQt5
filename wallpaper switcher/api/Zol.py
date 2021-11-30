from re import search, findall, sub
from requests import get

from . import BaseSpider


class Zol(BaseSpider):
    def __init__(self, father):
        super(Zol, self).__init__(father, self.__class__.__name__)
        self.start = 0

        self.b64_data = b'AAABAAEAEBAAAAEACABoBQAAFgAAACgAAAAQAAAAIAAAAAEACAAAAAAAAAAAAMQOAADEDgAAAAEAAAAAAABmAAAAANROAM//4gAApTAAuyIQAAH/rQBNORkAeI5HADbfZwCSEQkANclWADj/qQDJOR4ALeuQAINHHQD0ORsAJ/+sAP///wAB/24AP9F7AHIDAwBgxX4AYkAbAHDglAAA/+MAAL1AANUrFQDwNxoAAP/VAJNyMAAx/5EAJ3EkAAD/zAA/izYA/1w2AAH/lQBgMR4AoxoNACDcYgCRb0kAggoFACqVLgCcwXsAN5VhAHH/tAByTDoAYf+gAAD/vAAx/4QAAf97AOhWLABg/7kATFExAN4sFQAXvUcAhCgRAAH0ZgDEJxMAyE8hADvDpQDg9uYAiTY0AImTWAAB5lsAAK83AAH/pgBnXCUAOeOMAKMUCgA/tWEAsxwOAADMRQAO/30AYPmbAPpnUQBnDwkAD/+0ANVSKgAN/78AxTQeABvhoABzBwQAxCMRAA2vOgCMCAgAnBgLAMhJIwBXPRoA3//uAAH/jADmMBgAAd5VADC1WAAP/6EArx8PAIV5MgAO9WkAhKJXAAD/tgCTSh4AckUcAM8pFAD/Px4AAf+eAADEQwBrAAEAAP/FAACuMwCBk0kAAf91AGDRgQCsGw4AblA5AL9PLACJPzsAAM5LAAz/0QDdMRgAmxMKALYhEAB7CQUAjBAJAM4hEADZLhYApRkIAIcPCABzCAAAAPBcAAC3OwAA/+wAAP/gADP/mQAB/4AA5VctAGD/vADPSiIAAORUADDAWwAAxUoAAAAAAICAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAi4uLizwVXANriW48i4uLi4syAwNrQIAZaEdHUx8tUYuLSimAGWhzNiFCNyhpaWmLi3E6RwFbPx01Um8JeGkAizxjWl9/OBJghxoEJXlRAAIXDmVaCm0xhAhaZXdVeVFJJmQEZVZIWSMjbFo5XlV9MIgWJQRlB2dBQV1NdTleVRJ/VwklBBoTYi8vQw97OV5tMAZ4CW8EDE4gHC8+G3s5Hi4GACgJb1InGIIcTIUbeywCBmlpKHZGejuBHGoNZhtYiyRpaRR9RARPdCAvBWFmi4s9aWlLNCtQICAvBWdZIouLcnBFI0EFYmJiBWcLgyqLi4uLi1gzEGdnEIZYi4uLi/APAACAAQAAgAEAAIABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIABAACAAQAAgAEAAPAPAAA='
        self.cate = ['随机', '风景', '动漫', '建筑', '植物', '静物', '动物', '影视', '星座', '美食', '节日']
        self.true_cate = ['fengjing', 'dongman', 'jianzhu', 'zhiwu', 'jingwu', 'dongwu', 'yingshi', 'xingzuo', 'meishi', 'jieri']

    def a_page_spider(self, cate):
        page = ''.join(get('http://desk.zol.com.cn/{0}/{1}x{2}/{3}.html'.format(self.true_cate[self.cate.index(cate)-1], *self.father.resolving, str(self.father.data['api'][self.name]['cate_page'][cate]//21+1)), headers=self.headers, timeout=self.father.config['timeout']).text.split())
        lis = findall('<liclass="photo-list-padding"><aclass="pic"href="(.*?)"', page)
        if len(lis) < 21:
            self.down = True
        return ''.join(get('http://desk.zol.com.cn'+lis[self.father.data['api'][self.name]['cate_page'][cate]%21], headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall('<liclass="show.*?"><ahref=".*?"><imgsrcs?="(.*?)"', r)
        result = True if (new_set != self.img_set)and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data

    def a_img_spider(self, data):
        img = get(sub('\d*x\d*', '{0}x{1}'.format(*self.father.resolving), data), stream=True, timeout=self.father.config['timeout'], headers=self.headers)
        tail = search('.*?([jpnegJPENG]{3,4})"?', img.headers['Content-Type']).group(1)
        return img, tail
