from requests import get
from re import search, findall

from . import BaseSpider

class Visualhunt(BaseSpider):
    def __init__(self, father):
        super(Visualhunt, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAABILAAASCwAAAAAAAAAAAAC8vwr/vL8K/7y/Cv+8vwr/vsgz/8Hfk//E7tf/xfb3/8X18v/D7tP/wd+T/77JNP+8vwr/vL8K/7y/Cv+8vwr/vL8K/7y/Cv+8wBD/weCW/8X3+v/F9/z/xff8/8X3/P/F9/z/xff8/8X3/P/F9/r/weCa/7zBE/+8vwr/vL8K/7y/Cv+8wBD/w+i7/8X3/P/F9/z/xff8/5y6/P9MNfz/TDX8/5y6/P/F9/z/xff8/8X3/P/D6b3/vMAQ/7y/Cv+8vwr/weCX/8X3/P/F9/z/xff8/8X3/P+Elvz/TDX8/0w1/P+Elvz/xff8/8X3/P/F9/z/xff8/8Hgl/+8vwr/vsk0/8X2+f/F9/z/xff8/8X3/P/F9/z/YVz8/0w1/P9XSvz/YVz8/8X3/P/F9/z/xff8/8X3/P/F9vn/vsk0/8Hekv/F9/z/xff8/8X3/P/F9/z/uOT8/0w1/P9MNfz/c3v8/0w1/P+45Pz/xff8/8X3/P/F9/z/xff8/8Hfk//E7tb/xff8/8X3/P/F9/z/xff8/5y6/P9MNfz/YVz8/3yJ/P9MNfz/nLr8/8X3/P/F9/z/xff8/8X3/P/D7tP/xfb2/8X3/P/F9/z/xff8/8X3/P+Elvz/TDX8/3N7/P+Urvz/TDX8/4SW/P/F9/z/xff8/8X3/P/F9/z/xfTx/8X29v/F9/z/xff8/8X3/P/F9/z/YVz8/0w1/P+Movz/lK78/0w1/P9hXPz/xff8/8X3/P/F9/z/xff8/8X29v/E7tb/xff8/8X3/P/F9/z/uOT8/0w1/P9MNfz/lK78/6rP/P9MNfz/TDX8/7jk/P/F9/z/xff8/8X3/P/E7tb/wd6S/8X3/P/F9/z/xff8/5y6/P9MNfz/TDX8/6rP/P+/7fz/TDX8/0w1/P+cuvz/xff8/8X3/P/F9/z/wd6S/77IM//F9vn/xff8/8X3/P+Elvz/TDX8/0w1/P+45Pz/xff8/1dK/P9MNfz/hJb8/8X3/P/F9/z/xfb5/77IM/+8vwr/weCX/8X3/P/F9/z/YVz8/0w1/P9MNfz/xff8/8X3/P9ze/z/TDX8/2Fc/P/F9/z/xff8/8Hglv+8vwr/vL8K/7zAEP/D6Lv/xff8/8X3/P/F9/z/xff8/8X3/P/F9/z/xff8/8X3/P/F9/z/xff8/8Ppvf+8wBD/vL8K/7y/Cv+8vwr/vMAQ/8Hglv/F9/r/xff8/8X3/P/F9/z/xff8/8X3/P/F9/z/xff6/8Hgmv+8wRP/vL8K/7y/Cv+8vwr/vL8K/7y/Cv+8vwr/vcgy/8Hekf/E7tb/xfX1/8X19f/E7tX/wd6R/73IMv+8vwr/vL8K/7y/Cv+8vwr/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=='
        self.cate = ['随机', 'Music', 'Travel', 'Flower', 'Nature', 'Sea', 'Tree', 'Food', 'Sky', 'Snow', 'Happy']

    def a_page_spider(self, cate):
        return ''.join(get('https://visualhunt.com/photos/%s/%s'% (cate.lower(), str(self.father.data['api'][self.name]['cate_page'][cate])), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall('divclass="vh-Collage-item".*?<atitle=.*?href="(.*?)"><img.*?src="(.*?)\?s=s"', r)
        new_set = [[search('/.*?/(\d*)', x[0]).group(1), x[0], x[1]] for x in new_set]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        r = ''.join(get('https://visualhunt.com' + data[1]).text.split())
        resolution = findall('<input.*?downloadurl=".*?(\?.*?)?".*?<span>(\d*)x(\d*)\([\dSMXL]{1,3}\)', r)
        best = [100000, 100000, 0]
        for i in resolution:
            sub_ = [int(i[1])-self.father.resolving[0], int(i[2])-self.father.resolving[1]]
            if 0 <= sub_[0] < best[0] and 0 <= sub_[1] < best[1]:
                best = [*sub_, i[0]]
        if best[-1] != 0:
            img = get(data[2] + best[2], headers=self.headers, stream=True, timeout=self.father.config['timeout'])
            tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
            return img, tail
        else:
            return False
