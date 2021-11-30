from requests import get
from re import search, findall, sub

from . import BaseSpider

class V3wall(BaseSpider):
    def __init__(self, father):
        super(V3wall, self).__init__(father, self.__class__.__name__)
        self.start = 0

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABUElEQVR4nIWTsU7CUBSGv1YRJVBJumrAxM3RSRbr5gaTrPgGJn0AeQBJHNwYZK2LbLpZH8DRzQGCo6hcGSwkvQ6VS0tbOMlN/+Tknv87N3+1D64kS0ovG6yVtwGYuoNYX5u4AyksJ3WAKW2lh1orbrDMPWPtKj0+f0wmFJZDvnOa2DSezpT2Oq/JAwD0/x3T3MXJXSqlDpBEEXafugM2avuY0lYnMmCRIts4UPprr43h1incV6MGbj06IEyRvw2+cuTh9wTjxgN+XzDUWurECGYUuWZl7l5uA+D3hNIAhW6Vn1o3PkBYDluXR8pdfnsR7FyzgiltJt031dMWk2i4dTLHO4mhCZcpbYZaKx4kYTn4fbH0MsyDlZjE8L4Q7BwurZhVD72+ymnz4pCNapCBGZleMpAjL50gXL/XL0yf39VFvWTg9wWfxZuAZtXvvKr+ADuMf1yYfI/2AAAAAElFTkSuQmCC'
        self.cate = ['随机', '风景', '动漫', '影视', '动物', '植物', '节日']
        self.true_cate = ['1', '7', '5', '4', '3', '15']

    def a_page_spider(self, cate):
        page = ''.join(get('http://www.v3wall.com/html/pic_item/pic_item_%s_%s.html' % (self.true_cate[self.cate.index(cate)-1], self.father.data['api'][self.name]['cate_page'][cate]//20+1), headers=self.headers, timeout=self.father.config['timeout']).text.split())
        lis = findall('<divclass="s_p_list_pic"><ahref="(.*?)"', page)
        if len(lis) < 20:
            self.down = True
        return ''.join(get('http://www.v3wall.com'+lis[self.father.data['api'][self.name]['cate_page'][cate]%20], headers=self.headers, timeout=self.father.config['timeout']).content.decode().split())

    def a_page_finder(self, r, c):
        new_set = findall('<divclass="s_p_list_pic"><ahref=".*?".*?<imgsrc=".*?/(\d*)/small_(\d*\..*?)".*?<divclass="s_p_list_other">.*?>(\d*)x(\d*)', r)
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = [[search('(\d*)\..*?$', x[1]).group(1), 'http://www.v3wall.com/wallpaper/{0}_{1}/{2}/{0}_{1}_'.format(*self.father.resolving, x[0])+x[1]] for x in new_set] if (int(new_set[0][2]) >= self.father.resolving[0] and int(new_set[0][3]) >= self.father.resolving[1]) else []
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        img = get(data[1], headers=self.headers, stream=True, timeout=self.father.config['timeout'])
        tail = search('.*?([jpneg]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
