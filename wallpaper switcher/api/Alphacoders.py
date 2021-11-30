from re import findall, search
from requests import post, get

from . import BaseSpider


class Alphacoders(BaseSpider):
    def __init__(self, father):
        super(Alphacoders, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgBAMAAACBVGfHAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAJ1BMVEUAAAD4+Pj+/v6qqqr+/v739/f9/f37+/v7+/v9/f3///81fscAAACMxWBzAAAACnRSTlMAIfcCox5fND5lCFIUQwAAAAFiS0dEAIgFHUgAAAAJcEhZcwAALiMAAC4jAXilP3YAAAAHdElNRQfgCRQRFwrwSbdUAAAAc0lEQVQoz8WRwRGAIAwEmfGXEnxZgk3Yh6XxdEIBjklz5sCgYAHc44Ys+7sQfqH49rxYJQneU9rw1N1aASh3Uth6jgeydgBKC6QHOghEAnwAG2CjB/4YAIrlYlYBINYazuu4okX4KkUwpcbX9Tv63p3Q5gZJMK91/Bc8ugAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxNi0wOS0yMFQxNzoyMzoxMCswMjowMDdzJawAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTYtMDktMjBUMTc6MjM6MTArMDI6MDBGLp0QAAAAV3pUWHRSYXcgcHJvZmlsZSB0eXBlIGlwdGMAAHic4/IMCHFWKCjKT8vMSeVSAAMjCy5jCxMjE0uTFAMTIESANMNkAyOzVCDL2NTIxMzEHMQHy4BIoEouAOoXEXTyQjWVAAAAAElFTkSuQmCC'
        self.cate = ['随机', 'Nature', 'Scenery', 'Mountain', 'Food', 'Night', 'Forest', 'Landscapes', 'Literature', 'Movies', 'Music', 'Plants', 'Sea', 'Sky', 'Sports']
        self.cate_data = {'view': 'paged', 'min_resolution': '{0}x{1}'.format(*self.father.resolving), 'resolution_equals': '>=', 'sort': 'rating', }

    def a_page_spider(self, cate):
        return ''.join(post('https://wall.alphacoders.com/search.php?search=' + cate + '&page=' + str(self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, data=self.cate_data, timeout=self.father.config['timeout']).content.decode().split())

    def a_page_finder(self, r, c):
        new_set = findall('class="thumb-container-big"id="thumb_(.*?)".*?class=\'thumb-info-big\'><span>(\d*)x(\d*)', r)
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        id_, width, height = data
        box = self.cal_crop(*self.father.resolving, int(width), int(height))
        get('https://initiate.alphacoders.com/crop/{6}/{0}/{1}/{2}/{3}/{4}/{5}/0/English'.format(*box, *self.father.resolving, id_), headers=self.headers)
        r = post('https://api.alphacoders.com/content/get-download-link', headers=self.headers, timeout=self.father.config['timeout'],
                 data={'content_id': id_, 'content_type': 'crop_stretch', 'content_name': 'cropped-{0}-{1}-{2}.jpg'.format(*self.father.resolving, id_)})
        url = r.json()['link']
        img = get(url, stream=True, timeout=self.father.config['timeout'])
        tail = search('.*?([jpnegJPENG]{3,4})"?', img.headers['Content-Type']).group(1)
        return img, tail

    @staticmethod
    def cal_crop(r_w, r_h, w, h):
        if w / h >= r_w/r_h:
            mut = h / r_h
            space = int((w - r_w * mut) // 2)
            return space, 0, w - space * 2, int(r_h * mut)
        else:
            mut = w / r_w
            space = int((h - r_h * mut) // 2)
            return 0, space, int(r_w * mut), h - space * 2
