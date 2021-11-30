from requests import get
from re import search, findall

from . import BaseSpider

class Wallpapercave(BaseSpider):
    def __init__(self, father):
        super(Wallpapercave, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABTElEQVR4nJWTvUoDQRSFv5mg6bTw5zXEB7CyCEYQYmViUpqA4EPkFRQhu4WgEkdTaGcGfAFBCxFSKNgpIqaxVMyMhes4+5Ogt9lz55x77ll2FqIKguuxUGnLP0s6NNE/+euQv8gZCCglRaHSu6nhdrfgm8ikACA80gcR3NzZv5iKkYJYUgkQHJ+vAWC5ikS1H0F+fNCPG4jJlIGwsv3d2r2sRKNK+s+nu8swUN1tjze+OFD6cJgBAM1m0wjEljuwvPu8gOovxSOADJQ+zYpmsS8I8sOiCwaLANL/fKHSLaf4ZN4fCJV+9ft6efk+9QpAw4Ha0nOCm85KknkPGIjY9qDdbfi9NR8zIw3q1cJNBHsAQoqWzzfWV9zdSBtYs+ogppSkhTVzfi9zOTMb214pnrlN5eJD3NssbFSKt1mpCZV+63Q6uVQga8Wo3/wLwtpuEJDavakAAAAASUVORK5CYII='
        self.cate = ['随机', 'Animals', 'Anime', 'Cartoons', 'Geography', 'Holidays', 'Games', 'Movies', 'Nature', 'Space', 'Music']

    def a_page_spider(self, cate):
        all_page = findall('<divclass="aall".*?><divclass="albumphoto"href="(.*?)"title=".*?">', ''.join(get('https://wallpapercave.com/categories/%s' % cate.lower(), headers=self.headers, timeout=self.father.config['timeout']).text.split()))
        return ''.join(get('https://wallpapercave.com'+all_page[self.father.data['api'][self.name]['cate_page'][cate]], headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall(r'<aclass="download"href="(.*?)"><imgsrc="', r)
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return search('.*-(.*?)$', data).group(1)

    def a_img_spider(self, data):
        img = get('https://wallpapercave.com'+data, stream=True, timeout=self.father.config['timeout'], headers=self.headers)
        tail = search('.*\.(.*?)"$', img.headers['Content-disposition']).group(1)
        return img, tail
