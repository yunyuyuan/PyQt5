from requests import get
from re import search, findall, sub

from . import BaseSpider

class Wallpapersite(BaseSpider):
    def __init__(self, father):
        super(Wallpapersite, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAFMUlEQVR4nO2XaUxUVxiGnxnBGRGsoM6IVUt0GJZBG6BJjeDaRm3VGmOtFdSq4ILVVNui0VaTikvtCKYbLkSjYrVxqwzWpU3jhtaKS6woIFqJK05cYJDlsn39MeWW6Qz2Rxf94Zfc5Jz3vPc97/nud889V2MyW4QnGNonObmA44kagCecgafCgBdAZOSLBJtMbN+x699RVR5B10huDE5BMUaosP7WOQw/LKblvSIV05SU3BWj0aACwSER/JPQld3k2pelVJYD7cH7YhF6ewE1HcwohhAAWj4opuv6Yc4iNBoNVFVVkZ9fAEC7dgHNioeHhzFo0KuPNVCQVkrlfQg8nkaP5f3Qtain3DKcen0bAnfPpGPWbGoCgmho2dqZARERAHNoDy4XXCAn5wSTEqa6Ca+0fsqIN4apfU+ZuvfKfEoj44nOXcqFyCRqvJtfTPdV0VCnOLTZ2d8DoNfrAYiN7e3xhsbJj+UcB8AcHOzGKY2KByOUXC2gxisAaqHbF70xWSMwWSPQ2fMB8C08iKZOAUD7/ofzANi/L4tTp04D4OPj4yLcv19fANJWfc7khGkAbMnc4O6yDgJ+s1PVLQY0EJ2fjlZxqMNdNo3GZI2go+0DFVNfw+c7dSJ+/EQArCuWueiuXfMVAKvXZDDnvVkA+Pv7u3DatPGDCijt7EuHkrMgcL7bm+4m/xJagPT0tQB0aN8ewK3QtFotDx48ZFXqZ8yYMY0BrwwGYFz8WJWTal2BIRAaKn3wO58FL0BdawNXZ5+mvlXb5h2YzBYxmS0iIuJwlMuhQ0dERCQkrKeYzBZZv2GjiIjK8dRu7FfUNAipIthEgmJGivfKYiFD1Msw6mOVbzJbpLvZUuayE/r5+TJl2gwAli9LAWDypHcA6NKls8o79NNBTvx8Uu3r9ToA1qV/zdah1VAIxZN2o62uIGj1QDr8uBgA+5AUriTnUesf5J6B5LnzRUTktaEj3Fb6yeKlKnbv3n2Xsf0HDkqWLdsFK7HbRbuizGX1ga/PlM4Dx6v9zv3jpLvZUkbTlIiIKIoiNtteERHJLyh0EVYURUaMHC0iItOTZqmmqqqqRURk/oKFIiKSkDhd1fSbk+1ixGS2qG03Aw5HudszLi0rk6PHckREZPSYOJexxClJarsxg03roumlS7kgZIjollwUr7Q7QoaIcficKpcamDI1CYDoqEgVe7lXLH1iYwA4d+48ABcvXgLg8JGjKu+7PTYAbt265bHYu2S+DYBiDKdt7kYAaozhWhcDZ86eA+DbbZlszvwGAIvFAsDRYzkqL378JABse3Zy+/YdAOYlOzeXUROSPBpoGvU+7QDQ1lQ6P8dN43JREebgYFKWLKe6uppdO7YBkDjlT+GKigoAwsJCCQnrSd++sWSsTWfAPvjlLRu0AK1STqfd76K/eRbFGM6NCdsBMBxYiH2I8w3zvbS3xu1A0rjVJiZMJHPLVhX/45ulxrqM9QDEjR3DtWvFABz+Fbyq7AA06Py4OXYzV5Lz1Mk1dQo6e6Gq4eW43aDxdCouKswDoKDwMqEhZhZ8tIgdO3e7pbKRd/rMWV6KjkKTCjwHxr1zaXU9l7KoOBRjOF6P7tI2dxMVpgHc7zsbAJM1AgGHRwPjx8WxaOECtd/cIcW2ZydhYaEuvCvJeS4cTW014q13wUxWp16zBsD5fINNJmzZez1O3hh9YmPw9fVl/4GDKvYoZBAPe01FMTjNaepraXX9JO0Pp7kcxx5r4P+IZ/8Fzww8FQa8BBx/T/uvQhy/A57OyMAMQrmuAAAAAElFTkSuQmCC'
        self.cate = ['随机', 'Animals', 'Anime', 'Forest', 'Mountain', 'Flowers', 'Games', 'Movies', 'Music', 'Nature', 'Sports', 'World']

    def a_page_spider(self, cate):
        return ''.join(get('https://www.wallpapersite.com/'+cate+'/?page=' + str(self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall(r'<p><ahref="/.*?/(.*?)\.html"><imgsrc=".*?"srcset', r)
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return search(r'-?(\d*)$', data).group(1)

    def a_img_spider(self, data):
        url = ('https://wallpapersite.com/images/wallpapers/' + sub('-', '-%sx%s-' % (self.father.resolving[0], self.father.resolving[1]), data, count=1)) + '.jpg'
        img = get(url, stream=True, headers=self.headers, timeout=self.father.config['timeout'])
        tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
