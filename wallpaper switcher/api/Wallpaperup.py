from requests import get, post
from re import search, findall

from . import BaseSpider

class Wallpaperup(BaseSpider):
    def __init__(self, father):
        super(Wallpaperup, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'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'
        self.cate = ['随机', 'Abstract', 'Animals', 'Food', 'Sports', '3D', 'Dark', 'Anime', 'Cartoons', 'Movies', 'Drops', 'Flowers', 'Fruits', 'Lakes', 'Landscapes', 'Mountains', 'Plants', 'Rivers', 'Sea', 'Sky', 'Space', 'Trees', 'Waterfalls', 'Nature', 'Architecture', 'Cities']

    def a_page_spider(self, cate):
        return ''.join(get('https://www.wallpaperup.com/search/results/%s+resolution:%sx%s/%s' % (cate.lower(), self.father.resolving[0], self.father.resolving[1], self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall(r'<figureclass="black"><ahref="/(\d*)(.*?)"title="Viewwallpaper"class="thumb-wrp"', r)
        new_set = [[x[0], x[0]+x[1]] for x in new_set]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        id_, url = data
        img_url = search('<formaction="(/wallpaper/do_download/.*?)"method="post"class="card-footerborderedcustom"', ''.join(get('https://www.wallpaperup.com/'+url).text.split())).group(1)
        img = post('https://www.wallpaperup.com'+img_url, data={'height': self.father.resolving[1], 'width': self.father.resolving[0]}, headers=self.headers, stream=True, timeout=self.father.config['timeout'])
        tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
