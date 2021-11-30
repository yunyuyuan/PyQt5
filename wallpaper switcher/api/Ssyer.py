from time import sleep

from requests import post, session
from re import search
from requests.cookies import RequestsCookieJar

from . import BaseSpider

class Ssyer(BaseSpider):
    def __init__(self, father):
        super(Ssyer, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABl0lEQVR4nKVSv0ubURQ95933kr3EaIyDEBDBtkuGiiBCl0DJUAeFQEAUMmQopYNDoBSCQoeMGbIVAoVKHbp0yVTEDnEt1IKlpYPx04j/gfF2CO/Lj0bUeqb7Duecd+/lAvcER5G51LF++DXFXOpYoaiCuqrKBzu/pyLDWuOL/ExLfS2GW/mZlhrBd7GIiZjxUeaBALHA2sPWLAC8/5l8IxawlnNimRN7/Qh9AYQY/th4fKIAUD9Msn6YpFhCLOF5j/VHrT9hQCEd6LtvkxRHiCMK6UAL6UABoJ/32kI6UBsxX8MlFue74lozweKT4COIlf7fas0EvaafCzuoNRO0jnixeKo2gue1ZoIiZs06wvNeE49OOM8N7KC6P8GuwbhXT8/URVHvccTLpWDaOqK8x0tnOmNi+SUcYRibmXbY7tVVZ9wYOfPvSiPOzUxbK434SO8AStm2lrLdsFK2raVnp/lhjfnX1sPbz3GKI14vn6s4ghF7dKcAANj+NBbegnM4uHMA0L1SIwjKu7Gb5x6FrfzFwn8Zb4O/pn98TcpRxaMAAAAASUVORK5CYII='
        self.cate = ['随机', '风景', '自然', '清新', '简约', '山水', '创意']

        self.session = session()
        try:
            cookie = RequestsCookieJar()
            for i in self.father.data['api'][self.name]['save_cookie']:
                cookie.set(i, self.father.data['api'][self.name]['save_cookie'][i])
            self.session.cookies = cookie
        except KeyError:pass

    def a_page_spider(self, cate):
        return post('https://www.ssyer.com/apis/20001', headers=self.headers, json={'keywords': "%s" % cate, 'order': 1, 'page': {'showCount': 20, 'currentPage': int(self.father.data['api'][self.name]['cate_page'][cate])}}, timeout=self.father.config['timeout']).json()

    def a_page_finder(self, r, c):
        new_set = [[str(x['id']), x['width'], x['height']] for x in r['data']]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = [x[0] for x in new_set if (int(x[1]) >= self.father.resolving[0] and int(x[2]) >= self.father.resolving[1])]
        return result

    def get_id_fromdata(self, data):
        return data

    def a_img_spider(self, data):
        try:
            url = self.session.post('https://www.ssyer.com/apis/20301', json={'id': data, 'width': 0}, headers=self.headers, timeout=self.father.config['timeout']).json()
            url = url['data']['ossDownUrl']
        except KeyError:
            if self.login() == 1:
                return self.a_img_spider(data)
            else:
                return 'break'
        img = self.session.get(url, stream=True, timeout=self.father.config['timeout'])
        tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail

    def login(self):
        self.father.verify.exec_signal.emit()
        while True:
            sleep(0.05)
            if self.father.verify.result != 0:
                return self.father.verify.result

    def download_code(self):
        r = self.session.post('https://www.ssyer.com/apis/104?rander=1569978139598', headers=self.headers, timeout=self.father.config['timeout'])
        with open('image/v.png', 'wb') as fp:
            fp.write(r.content)

    def verify_code(self, v):
        self.session.get('https://www.ssyer.com/login', headers=self.headers, timeout=self.father.config['timeout'])
        # TODO input your account
        s = self.session.post('https://www.ssyer.com/apis/101',
                              json={'imgCode': "%s" % v, 'method': 1, 'password': "d67e4fd0f0ebc4bf11c155b1f8930465", 'userName': "13227697053"}, headers=self.headers,
                              timeout=self.father.config['timeout'])
        if s.json()['code'] == 200:
            # 存储
            self.father.data['api'][self.name]['save_cookie'] = self.session.cookies.get_dict()
            self.father.dump_data('data')
            return True
        else:
            return False