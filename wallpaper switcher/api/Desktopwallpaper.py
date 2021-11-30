from requests import get
from re import search, findall, sub

from . import BaseSpider

class Desktopwallpaper(BaseSpider):
    def __init__(self, father):
        super(Desktopwallpaper, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'AAABAAEAEBAAAAEAGABoAwAAFgAAACgAAAAQAAAAIAAAAAEAGAAAAAAAAAAAAEgAAABIAAAAAAAAAAAAAAD////9/f3////////+/v7////////+/v7////////+/v7////////////////+/v7+/v7////////8/Pyqqqr////9/f2tra3////+/v7Jycni4uKrq6urq6v+/v7////+/v7+/v7+/v7///87OzvT09PV1dU6Ojr////z8/NwcHCdnZ1HR0dYWFjJycn+/v7///////+Pj49xcXE8PDyBgYHW1tY7OzuOjo5WVlZ2dnYuLi50dHSdnZ3h4eH///////////+AgIBLS0s5OTmenp7U1NQ7Ozs8PDw6OjpHR0cuLi5ISEhISEifn5/9/f3////9/f309PRHR0c8PDzU1NTX19ctLS1HR0ePj48uLi6ZmZk+Pj47OzvV1dX+/v7////9/f3///+dnZ0uLi7T09PV1dUtLS2enp7w8PA8PDyenp7h4eHj4+P+/v7////////////+/v7///+Ojo7z8/Px8fGPj4/////+/v6cnJzHx8f////+/v7////+/v7////////+/v6qqqqenp7FxcX////+/v7+/v7j4+PIyMj9/f2rq6v+/v7////////+/v7///////88PDxycnI+Pj6bm5v///////+CgoJjY2PIyMg7Ozvj4+P////9/f3////+/v7+/v4+Pj7U1NScnJxYWFj///////9WVlY8PDybm5suLi6rq6v+/v7///////////////86OjrV1dXV1dU9PT3+/v7x8fE8PDw7OztKSko6OjqQkJD////////9/f3///////89PT3U1NS6uro6Ojr///+3t7c8PDxzc3MqKiqCgoJVVVX///////////////////85OTmcnJxXV1eQkJD+/v6dnZ1ycnKenp48PDzU1NQ8PDz////9/f3////+/v7///+RkZFzc3OQkJD///////+enp7Gxsbx8fGcnJz///+NjY3x8fH////+/v7////////+/v7////+/v7////+/v7+/v7////+/v7////9/f3////+/v7///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        self.cate = ['随机', 'Animals', 'Abstract', 'Cartoons', 'Fantasy', 'Funny', 'Flowers', 'Holidays', 'Music', 'Nature', 'Photography', 'Sports', 'World']

    def a_page_spider(self, cate):
        return ''.join(get('http://www.desktopwallpapers4.me/%s/%s.html' % (cate.lower(), self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall(r'<divclass="img"><ahref="/.*?/(.*?)(\d*)/"', r)
        new_set = [[x[1], 'http://cdn.desktopwallpapers4.me/wallpapers/{0}/{1}x{2}/5/{3}-{4}{1}x{2}-{5}-wallpaper.jpg'.format(c.lower(), *self.father.resolving, x[1], x[0], sub('s$', '', c.lower()))] for x in new_set]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        id_, url = data
        img = get(url, stream=True, timeout=self.father.config['timeout'], headers=self.headers)
        tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
