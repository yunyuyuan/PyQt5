from requests import get
from re import search, findall

from . import BaseSpider

class Wallpaperhi(BaseSpider):
    def __init__(self, father):
        super(Wallpaperhi, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACkElEQVR4nGWTv4tUVxTHP/fOnfdjfrx5s7o/XFQksImFgWCVajcYCNhaiZWFVYhYClpYaqGBhTQh0crCLgEhkCKQPyAoFkoQE5JV1x1n1pl15s17M/PuPRZvmXF3b3cu53vO+X6/fNXa2pqw7znnWPl1jkQSOrZFciHEmwQopfa3YvZ/fP7LUUaSse3a7LgubdcivZtSP7dCvV4/MEB/XDS+ChlJxn8PN3nxdY/t512G/SG2KzjnDoD3DBARlq9E/PvwFZ31jDiO6Td6TF4K3Gnged60L/2sh7UWEZlROPnjEVIZ0rqdEMcxr28+IW8LtivMPV3Ar/kAbP78CGUU6n6dud+OFxeICGZRk0lKEBRiWXIkFbz1ecIwROsZW8kF8yBGa11ccOxqk0yGdP7ukq+3eDPfgy0o3WsyP16iHJSn4Oj8p1hrqTVrGGOKAf6XikxSbG3EaCGB91C+vERNR/h1f49o1Wq1EG/3IuOdtbxzHTJJGS71mfzk4z9YptFoUCqV9oDtasLg21cMXcLi+S8KCsnFLfrWMpKM7EzMoSMLbN97Tiv6H+0rKjeOEm8sFNu+S1BOIZcOzWwcfFPhne0wSAeUY8PbW8+wKodJIdb4r5nNmWRkkuJtVGcU/NOK/obDpTC69g/yGnTL4FYsugLVXf+dc3QGbVwfovJMVHXq+ieyc3oLGSrUUBP/cIIwDNm8/BQ8QVdA+UUGZCy4BHC78SkrjCBTcOX7ZaLDEZPFFN6WUDVBeuAqblp/HCfze4SJ/1ym7+1QehLSbDYxxqDbVbzHdfSSQ/9RJXRVgiAgz3N6UYfym5AgCAjDELW6uirj8RgRwff9aWQnkwnW2sIqY9BaIyLkeV5sNwalFB8AVzYikTiryCUAAAAASUVORK5CYII='
        self.cate = ['随机', 'nature', 'animals', 'Landscapes', 'anime', 'Clouds', 'mountains', 'fantasy', 'Trees', 'Flowers', 'Music', 'movies', 'sunset', 'snow', 'forest']

    def a_page_spider(self, cate):
        return get('http://www.wallpaperhi.com/tagged_wallpapers-%s/page_%s/rate' % (cate, self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, timeout=self.father.config['timeout']).text

    def a_page_finder(self, r, c):
        new_set = findall(r'<a\shref=".*?_(\d*)x(\d*)_wallpaper_(\d*)"><img\ssrc="/thumbnails/cover/(.*?)"', r)
        empty = False if new_set else True
        new_set = [x for x in new_set if int(x[0]) >= self.father.resolving[0] and int(x[1]) >= self.father.resolving[1]]
        result = True if (new_set != self.img_set) and not empty else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[2]

    def a_img_spider(self, data):
        w, h, id_, url = data
        img = get('http://cdn.wallpaperhi.com/%sx%s/' % (w, h)+url, stream=True, timeout=self.father.config['timeout'], headers=self.headers)
        tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
