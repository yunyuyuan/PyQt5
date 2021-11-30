from requests import get
from re import sub, search

from . import BaseSpider

class Unsplash(BaseSpider):
    def __init__(self, father):
        super(Unsplash, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAACwAAAAsCAYAAAAehFoBAAABA0lEQVRYhe2YLY4CQRBGH+yEgIEEgcDAAdZgSBBcgNvsDbgLmgPgcBg0GA6AWYWATTazpBJWkIDobygmk9TT80297qR/qmtozICFmDVyYAIcUoOZWLABdMVsodp1sdifmPsnV/+hCpdGCHsTwt6EsDdlCasnrCz8oRa8UVNrqyPtA9PbiaVgp9wKOIn5IAiCJ9i2tgY6iRNkma8Ck2p78BIYJuZ21qaMgVZi8Jj4/SNGwCAxk9lIz0KxH83xjouSicuPNyHsTQh7E8LeqMK/Bb1ytVtRXy8/gXmBFstyPTX4/YKn03exjUXnTQh7E8LehLA3lRRO7ZjLpGl3iQ3QroQu7K92EBq06X/VPgAAAABJRU5ErkJggg=='
        self.cate = ['随机', 'Nature', 'Sky', 'Night', 'Scenery', 'Forest', 'Tree', 'Architecture', 'Animals', 'Landscapes', 'Travel', 'Food', 'Sport']

    def a_page_spider(self, cate):
        return get('https://unsplash.com/napi/search/photos?query='+cate.lower()+'&per_page=20&page=' + str(self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, timeout=self.father.config['timeout']).json()

    def a_page_finder(self, r, c):
        new_set = [[str(x['id']), x['width'], x['height'], sub(r'\?.*', '', x['urls']['raw'])] for x in r['results']]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = [[x[0], x[3]] for x in new_set if int(x[1]) >= self.father.resolving[0] and int(x[2]) >= self.father.resolving[1]]
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        img = get(data[1] + '?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&fit=crop&h=%s&w=%s&cs=srgb.jpg' % (self.father.resolving[1], self.father.resolving[0]), headers=self.headers, stream=True, timeout=self.father.config['timeout'])
        tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
