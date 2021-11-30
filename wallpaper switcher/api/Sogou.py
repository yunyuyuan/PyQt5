from requests import get
from re import search
from urllib.request import quote

from . import BaseSpider

class Sogou(BaseSpider):
    def __init__(self, father):
        super(Sogou, self).__init__(father, self.__class__.__name__)
        self.interval, self.start = 10, 0

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACUElEQVR4nHVTP0jVYRQ99/fsLwTVUzJqsUwt0nIOmlpaaklCCtSWSDF7/hmkP2JlEfgna2lwCAsXWxqKlmaHttAy0cwokyTLhBT97jkNj97zvfRbPvjuvefec879DFlH948MAKgEBZBI31yGvNyujr9bnW+pwoelpfDYW4gA2WxNw12p2K2iAoivIBTBOWo3Px7MAFDv0UOgRkB/bU3DJ7KnSgG1FuYhCt9BzdndqXgaoLtMcH9tLSOpYt0uOglnMYRZyN9Y++QYAKgCMRTsDSAfWOd0g6nr8ACISmsZToLdLv4DaUsm/5QOK3bvy0Yl8s8DeGI9MxbBVYmw0pzkeuAlyC1wB5x3rH3C7NakoeNTBOcFuPoBwHpmnsoJ1eVVme6WyFpHk93bCx+DrFrVuRtLvGY9Xxaz9fC6+DRcsxEC05a0jVcj8COcgBMIbETEP0rsll/e9TwDIXDInGURnBnv1vFpv92ZMqyEeoTwU07IHUaeYm1c6RE8V+6/TNcLBPo+6/g8uZ59rMvVPzHNQ7H1LYyxZptE9ucg+DKoVwCK1bxHICEKIkdBfgB1DM6UG9a3MKY2RJp0RIs5iQhAOcgi1efnWedXQ/AbCmHRnCXmPG3OXLhDwZ9FffPJzZ3YVKNA2uDvueTSXMl/z4ZdUgVi69H4z4WzGzqzbMn7wdq4dGn7+bUK1IZIlZvPAYBX5IzzTEzAqs8EAH5xR69Rl0FCrm+gD4HINfE4KMhJiI+MqrUl7rQX+GlrdqveWkVXowllIudBPY98OWGDmMvO/QtY1nrJmXnXpgAAAABJRU5ErkJggg=='
        self.cate = ['随机', '世界风光', '动物', '动漫', '唯美', '风景', '清新', '静物', '手绘', '创意']

    def a_page_spider(self, cate):
        return get('https://pic.sogou.com/pics/channel/getAllRecomPicByTag.jsp?category=%s&tag=%s&start=%s&len=10&width=%s&height=%s' % ('%E5%A3%81%E7%BA%B8', quote(cate.lower()), self.father.data['api'][self.name]['cate_page'][cate], self.father.resolving[0], self.father.resolving[1]), headers=self.headers, timeout=self.father.config['timeout']).json()['all_items']

    def a_page_finder(self, r, c):
        new_set = [[str(i['id']), i['pic_url']] for i in r]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        id_, url = data
        img = get(url, stream=True, headers=self.headers, timeout=self.father.config['timeout'])
        tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
