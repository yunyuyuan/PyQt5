from requests import get
from re import search, findall

from . import BaseSpider

class Huyanbizhi(BaseSpider):
    def __init__(self, father):
        super(Huyanbizhi, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADDUlEQVR4nFWTzWtcZRTGf+/Hvbn3TmZuphnz0UwyFCk2rVIC9mPhVxUsCIoGtAsR3LhT/wIFUcGNdOMiFqRuFF20C8G60LoRrUpaq0KKGJLGNNXmYzKZ78m9931fFxPEns1zeBbn4TznPGL2s5VbN3eSwoCSWOcAEICUAgH0mf+VAwvsZpZ7i35Dr+yk5UhLNjsZkSeRQtDLLJ4UIKDWNf0eMM4hhWDQlwwFiuVaUtBa0mgktvDWqVGOjAQkpq/50bVtfr3TY+7pMYZDhQB6xhFqQTdzvPntOggaspVYZsYCHprKcfbKFq9+eZtWYnhuOub1EyXGBzVfLTa5vNzikUoOLQWf/LZDYhy+lOjMOQZ9SSe1FEPFZOzhK0lmLXEgmZuv8vH1GsbCiXLET2sdzv+yzclyBBKktYAQxIHiqYN5zj1TJu9Lzl7ZxFOQ9xUjOU0cSLY6hiMjAYUBxd6maGNhsuDx460OCxs91lsZvhIcKgVkBgZ9SSlSdFPJdjfj+ETEeF4jBDgHOrUOLWEq9hjJaV66uMrpg3mePVSgkzpeO1nizAMxICgGitFBxYUzFebmq1z6s4k21pH3Fav1FE8J3j89ztSQz/ztDvcND/D9X23OX69xT6QAeOeJUb5eanL17y7FUKEnCh6XFpvUuhn78x6PHcixWN3l09/rfP7CFNf+afDNUpNK7LPeznjlwX20E8tidZfpUoD2lWBho8fbj49ydCxgq2PIjGO5ltJOLKGWlCLNcKSo7xpWainHyxFKCiwOqYQg1IILC3U++LnKe99tEHqS5++PSa2j1jWsbSfUe4Z9oeKH1TaV2Kec90iMQ1a7GTPjIbOHY47tDzl1IEe54LHdMbQTy4tHh3j3yTEeruRwDi4vtSiGipdnitxpZmjjQIr+FYSAaRFwY7PHxRt1uqnljUdHmD0c88UfDTLXJjOOc1erSAEDWiCOfbjoANbb2V2hGwr6rjd2DVIIcnsBAlhvpUSeREuBnoy9teVaUpgoeHcNEHuY8+R/hLH99xuONN3UUom9xr8VqjoV69KR9AAAAABJRU5ErkJggg=='
        self.cate = ['随机', '风景', '动漫', '星空', '大自然', '星座', '植物', '艺术', '音乐', '节日']
        self.true_cate = ['fengjing', 'dongman', 'xingkong', 'daziran', 'xingzuo', 'zhiwu', 'yishu', 'yinyue', 'jieri']

    def a_page_spider(self, cate):
        return ''.join(get('http://www.huyanbizhi.com/%s/%s.htm' % (self.true_cate[self.cate.index(cate)-1], self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall('<lidata-like=.*?><ahref="/bizhi/(\d*)\.htm"', r)
        new_set = [[x, 'http://www.huyanbizhi.com/bizhi/'+x+'.htm'] for x in new_set]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        page = ''.join(get(data[1], timeout=self.father.config['timeout'], headers=self.headers).text.split())
        w, h = search('<ul><li><ahref=.*?rel="nofollow".*?>(\d*)x(\d*)', page).groups()
        if int(w) >= self.father.resolving[0] and int(h) >= self.father.resolving[1]:
            img = get(search('</span></a><ahref="(.*?)".*?><span>立即下载', page).group(1), headers=self.headers, stream=True, timeout=self.father.config['timeout'])
            tail = search('.*?([jpneg]{3,4})$', img.headers['Content-Type']).group(1)
            return img, tail
        else:
            return False
