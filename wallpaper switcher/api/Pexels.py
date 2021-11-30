from requests import get
from re import search, findall

from . import BaseSpider

class Pexels(BaseSpider):
    """ Pexels """
    def __init__(self, father):
        super(Pexels, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'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'
        self.cate = ['随机', 'green', 'trees', 'sky', 'mountains', 'flowers', 'black-white', 'scenery', 'rain', 'food', 'water', 'mockup', 'river', 'landscape', 'clouds', 'earth', 'night', 'winter', 'sport', 'sea', 'forest', 'nature', 'sunset', 'wood', 'architecture', 'travel']

    def a_page_spider(self, cate):
        return ''.join(get('https://www.pexels.com/search/'+cate+'/?page=' + str(self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall(r'data-photo-modal-download-value-original=\'(\d*)x(\d*)\'.*?data-photo-modal-image-download-link=\'(.*?)\?.*?data-photo-id=\'(\d*?)\'', r)
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[-1]

    def a_img_spider(self, data):
        width, height, url, id_ = data
        # 筛选: 分辨率比屏幕大
        if int(width) >= self.father.resolving[0] and int(height) >= self.father.resolving[1]:
            img = get(url + '?crop=entropy&cs=srgb&fit=crop&fm=jpg&h=%s&w=%s' % (self.father.resolving[1], self.father.resolving[0]), headers=self.headers, stream=True, timeout=self.father.config['timeout'])
            tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
            return img, tail
        else:
            return False
