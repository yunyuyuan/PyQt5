from requests import get
from re import search, findall, sub

from . import BaseSpider

class Hddesktop(BaseSpider):
    """ 百度 """
    def __init__(self, father):
        super(Hddesktop, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'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'
        self.cate = ['随机', 'Animals', 'Anime', 'Flowers', 'Games', 'Night', 'Movies', 'Landscape', 'Forest', 'Mountain', 'Scenery', 'Nature', 'Sports']

    def a_page_spider(self, cate):
        return ''.join(get('http://hddesktopwallpapers.in/page/%s/?s=%s' % (self.father.data['api'][self.name]['cate_page'][cate], cate), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall(r'<imgwidth="\d*"height="\d*"src="(.*?/\d{4}/\d{2}/)(.*?)(\.[a-zA-Z]{3,4})"class="alignleftwp-post-image', r)
        new_set = [[x[0], sub(r'-\d*x\d*', '', x[1]), x[2]] for x in new_set]
        new_set = [[''.join(x), x[1]] for x in new_set]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[-1]

    def a_img_spider(self, data):
        url, id_ = data
        img = get(url, stream=True, timeout=self.father.config['timeout'], headers=self.headers)
        tail = search('.*?/([jpneg]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
