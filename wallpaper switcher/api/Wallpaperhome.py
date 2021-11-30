from requests import get
from re import search, findall, sub

from . import BaseSpider

class Wallpaperhome(BaseSpider):
    def __init__(self, father):
        super(Wallpaperhome, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAb5JREFUeNrMk71LXEEUxc8dd7NqNMviKkrwMwoWIaL4F0jQxkIIaGGRwkqTRgVrG9tUKiwqQmKpYGFhkS6FrBCwsBPFDzaiSBDFRXfnzXhmfMIDSwt9cGZ4cy+/uffc98Rai+c88uKA2PWc5LhXU0vKYPQ8/Q75dCX+nLZsjGbHekUFRcB+grX70tEJpFJAEGwzv5v6p7gcUXHqi2ExtWVXaE/m3gw1bn1uqjyN2yBWztj3yKVpqstVT/12gPlIoF1zyWsMpxI60Ve3A5iYiw1GAA5WQrneZxxglbrzRMEwlE/65qzpqd01EMPqUQeRj1AMWvs1BJ1Qey79ltr1jgoGqBjZHd4gCX4RevMAlxHuFVRjCFh2iwpf1uIsau8MrduHmE7E4eq2gVUT3P/6bnWhn7ePh727TmejgJ9KYC7zKBWFyfDsgPpPLYoi/eKkBbfXU74NgObgIgrIcQLHhnlN9SjV2p8thF/IGoy5oxcK5W8rYPxp5tHRRwAKBawna4CqKjdmaHqxVPQTkLwtFrKo/wAkGTSB82zlCYDgzPtmaLbirsi6ErVVfliE/ZCGNhOObjM0/pX8C88G3AswAFXgnMgRrxmJAAAAAElFTkSuQmCC'
        self.cate = ['随机', 'Animals', 'Abstract', 'Architecture', 'Games', 'Movies', 'Music', 'Nature', 'Sport', 'Space', 'Food', 'Holidays']

    def a_page_spider(self, cate):
        return ''.join(get('https://wallpapershome.com/'+cate+'/?page=' + str(self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        re = findall(r'<p><ahref="(.*?)"><imgsrc="', r)
        new_set = [[search('-(\d*)\.html$', x).group(1), search('.*?/([^/]*?)\.html', x).group(1)] for x in re]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        url = ('https://wallpapershome.com/images/wallpapers/' + sub('-', '-%sx%s-' % (self.father.resolving[0], self.father.resolving[1]), data[1], count=1)) + '.jpg'
        img = get(url, stream=True, timeout=self.father.config['timeout'], headers=self.headers)
        tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
