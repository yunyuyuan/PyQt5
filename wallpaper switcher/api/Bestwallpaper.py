from requests import get
from re import search, findall, sub

from . import BaseSpider

class Bestwallpaper(BaseSpider):
    def __init__(self, father):
        super(Bestwallpaper, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA30lEQVR4nGM8rhn5n4ECwMTAwMAgHuECFxCPcIHziWEzUsUFA2oAw8eTV/9jA8c1I7Gyny3cBuf//vT1P9wF1xJaGE5oRRG0UDLOk0E00I6BgYGB4cWi7dhdALMFJvd4ypr///////92z+n////////l+gO4y+AueL3+EMOTqWvhtjAwMDC8WLyDgYGBgUEmO5iBgYGB4WHHYgYGBgYGbg15uIsQBmyEGPDn8zcGBgYGBj4zLYZ3e8/AFX698ZDh59PXGF5igTG0FtSgSHw6dQ2FD7MdBmCGD5KENLTzAgCKP7G7JrpUYAAAAABJRU5ErkJggg=='
        self.cate = ['随机', 'Abstract', 'Animals', 'Cute', 'Creative', 'Flowers', 'Design', 'Games', 'Movies', 'Nature', 'World']
        self.true_cate = ['3D-and-Abstract', 'Animals-and-Birds', 'Cute', 'Creative-and-Graphics', 'Flowers', 'Vector-and-Design', 'Games', 'Movies', 'Nature-and-Landscape', 'Travel-and-World']

    def a_page_spider(self, cate):
        return ''.join(get('https://best-wallpaper.net/%s_desktop_wallpapers/page/%s' % (self.true_cate[self.cate.index(cate)-1], str(self.father.data['api'][self.name]['cate_page'][cate])), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall(r'<divclass="img_list_item"><ahref="(.*?)"><imgsrc="', r)
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return search('/(.*?)\.html', data).group(1)

    def a_img_spider(self, data):
        r = ''.join(get('https://best-wallpaper.net'+data, headers=self.headers, timeout=self.father.config['timeout']).text.split())
        resolution = findall('<ahref="(http.{0,200})"title="Download(\d*)x(\d*).*?>\d*x\d*.*?</a>', r)
        best = [100000, 100000, 0]
        for i in resolution:
            sub_ = [int(i[1]) - self.father.resolving[0], int(i[2]) - self.father.resolving[1]]
            if 0 <= sub_[0] < best[0] and 0 <= sub_[1] < best[1]:
                best = [*sub_, i[0]]
        if best[-1] != 0:
            img = get(best[2], headers=self.headers, stream=True, timeout=self.father.config['timeout'])
            tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
            return img, tail
        else:
            return False