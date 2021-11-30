from re import search, findall, sub
from requests import get, post

from . import BaseSpider


class Wallpapertag(BaseSpider):
    def __init__(self, father):
        super(Wallpapertag, self).__init__(father, self.__class__.__name__)
        self.start = 0

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABAUlEQVR4nKWTMWqEUBCGv1UIVove4VWSgOAlbKy0Ug8geAXxAFYJpPIognuKpLHxBoIpxCIwKURYVt1NzMDAK2a+988wP8zxDsgf8ht44mDzdXJaHgfjjT16WZYSRZEAIiJ7Cr52AcMwiKZpjwCyCVBKiYiIUkrCMJSmaUQptQnQboeK45gsywDIsoyiKBjHkSAIdhexopqmKW3bCiB934uu67sjrBS4rkue59R1jeu6WJaF4zgYhrH5+wrgeR5JkjBNE77vA+D7PrZt/36EZevn81m6rrt7TCsF15GmKVVV3Sv59yV+npiNoR8EvMDsqiNGutzSXplv+1HjB/C8NP0A6+W+hsDRAoAAAAAASUVORK5CYII='
        self.cate = ['随机', 'abstract', 'holidays', 'animals', 'anime', 'art', 'movies', 'music', 'nature', 'space', 'fantasy', 'flowers', 'travel']
        self.true_cate = ['12', '24', '13', '14', '11', '27', '40', '29', '31', '18', '19', '42']

    def a_page_spider(self, cate):
        page = ''.join(post('https://wallpapertag.com/api/collection/%s/60/%s' % (self.father.data['api'][self.name]['cate_page'][cate]//60, self.true_cate[self.cate.index(cate)-1]), headers=self.headers, timeout=self.father.config['timeout']).text.split())
        lis = findall('<divclass="columncollection_thumb"><a.*?href="(.*?)"', page)
        if len(lis) < 60:
            self.down = True
        return ''.join(get(lis[self.father.data['api'][self.name]['cate_page'][cate]%60]).text.split())

    def a_page_finder(self, r, c):
        new_set = findall('<divid="(\d*)"data-fullimg="(.*?)"data-or="(\d*)x(\d*)"', r)
        empty = False if new_set else True
        new_set = [x for x in new_set if int(x[2]) >= self.father.resolving[0] and int(x[3]) >= self.father.resolving[1]]
        result = True if (new_set != self.img_set)and not empty else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        img = get('https://wallpapertag.com'+data[1], headers=self.headers, stream=True, timeout=self.father.config['timeout'])
        tail = search('.*?([jpnegJPENG]{3,4})"?', img.headers['Content-Type']).group(1)
        return img, tail
