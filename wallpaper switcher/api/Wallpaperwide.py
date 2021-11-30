from requests import get
from re import search, findall

from . import BaseSpider

class Wallpaperwide(BaseSpider):
    def __init__(self, father):
        super(Wallpaperwide, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABC0lEQVR4nNXSvy5EURDH8c/evchmgwTRaMSfRiehElFoaCQkim2UWm8g8RAKL8ADqEQUJAqVBIWITiFUsruJxt5V3CE3VzzATjI5J9/85pzfTIaej0qc89jASLCfTAr3Nk5xGTU7SFOMYxdXeEYfVjCMY3QjZ9HAE14xhiqs4qDkbBJHqJf4fuh/O0gwiFZJ2IyzVuKt0qPdBFn0CjNYDyZ4ir0o7Ba0W1hO8YKBgFNYxDnuwkkNcxjFPd5CO4H+FLeRCm6+cBisWnBzUbDfQZLIJ74UsO3v4D5DPFTidbRTrMWP13gMyw08hLCCd2zKB96JVqdxUpEvT4aPKFjAtnwPsn+yiTPc6P34BvY5ODUvaGTHAAAAAElFTkSuQmCC'
        self.cate = ['随机', 'animals', 'architecture', 'black_white', 'cartoons', 'food', 'forest', 'funny', 'games', 'holidays', 'landscapes', 'mountain', 'movies', 'nature', 'seasons', 'sports', 'scenery', 'travel', 'water']

    def a_page_spider(self, cate):
        return ''.join(get('http://wallpaperswide.com/%s-desktop-wallpapers/page/%s' % (cate.lower(), self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall(r'liclass="wall".*?<ahref="/(.*?)-wallpapers\.html"title="', r)
        new_set = [[x, 'http://wallpaperswide.com/download/%s-wallpaper-%sx%s.jpg' % (x, self.father.resolving[0], self.father.resolving[1])] for x in new_set]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        id_, url = data
        img = get(url, headers=self.headers, stream=True, timeout=self.father.config['timeout'])
        tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
