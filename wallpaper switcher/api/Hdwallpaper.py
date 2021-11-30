from requests import session
from re import search

from . import BaseSpider

class Hdwallpaper(BaseSpider):
    def __init__(self, father):
        super(Hdwallpaper, self).__init__(father, self.__class__.__name__)
        self.interval, self.start = 60, 0

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAoElEQVR4nGNgGPKA8X4kw39yNSsuZ2BkYmBgYFBYhmkGTIxDw5ZBYdl/OJZsOg5Xcz+S4T8TsbY9iGJkeBDFyMAqoYpiIdEGwMCjNBGGT7umMEj33WJgYGBgYEF3MjHg3YJcuHq4AQ+iGFEUEWsgyV5gYGBgEEqYzPD7xW1UFxALpPtuMbBKqMJdTLQBMC/9vHOC4UGUGlyc4oRErt5BBAA4TjGg3+f8lwAAAABJRU5ErkJggg=='
        self.cate = ['随机', 'mountain', 'sport', 'sunset', 'clouds', 'tree', 'water', 'nature', 'abstract', 'scenery', 'landscape']
        self.session = session()

    def a_page_spider(self, cate):
        return self.session.get('https://hdwallpapers.cat/api_json/tag/%s/%s' % (cate, self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, timeout=self.father.config['timeout']).json()

    def a_page_finder(self, r, c):
        new_set = [[x['id'], '-'.join(x['title'].split())+'-'+x['id']] for x in r]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        self.session.get('https://hdwallpapers.cat/'+data[1], headers=self.headers, timeout=self.father.config['timeout'])
        img = self.session.get('https://hdwallpapers.cat/wallpaper/'+data[1]+'.jpg', headers=self.headers, stream=True, timeout=self.father.config['timeout'])
        tail = search('.*?([jpneg]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
