from requests import get, session
from re import search, findall

from requests.cookies import RequestsCookieJar

from . import BaseSpider

class Pixabay(BaseSpider):
    def __init__(self, father):
        super(Pixabay, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'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'
        self.cate = ['随机', 'Animals', 'Architecture', 'Forest', 'Scenery', 'Mountain', 'Sky', 'Night', 'Food', 'Landscapes', 'Nature', 'Sports', 'Transportation']

        self.session = session()
        try:
            cookie = RequestsCookieJar()
            for i in self.father.data['api'][self.name]['save_cookie']:
                cookie.set(i, self.father.data['api'][self.name]['save_cookie'][i])
            self.session.cookies = cookie
        except KeyError:pass

    def a_page_spider(self, cate):
        return ''.join(get('https://pixabay.com/images/search/%s?pagi=%s' % (cate, str(self.father.data['api'][self.name]['cate_page'][cate])), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall('divclass="item".*?<ahref="/.*?/(.*?)/">', r)
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return search(r'.*?(\d*)$', data).group(1)

    def a_img_spider(self, data):
        url = data
        img = self.session.get('https://pixabay.com/tr/images/download/'+url+'.jpg', headers=self.headers, stream=True, timeout=self.father.config['timeout'])
        try:
            tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        except AttributeError:
            if self.login() and not self.father.switch_frame.abort:
                return self.a_img_spider(data)
            else:
                return 'break'
        return img, tail

    def login(self):
        page = ''.join(self.session.get('https://pixabay.com/zh/accounts/login/?source=main_nav&next=/zh/', headers=self.headers, timeout=self.father.config['timeout']).text.split())
        self.headers.update({'referer': 'https://pixabay.com/zh/accounts/login/?source=main_nav&next=/zh/'})
        # TODO input your account
        r = self.session.post('https://pixabay.com/zh/accounts/login/', headers=self.headers, timeout=self.father.config['timeout'], data={'username': "c1607439239@gmail.com", 'password': "cq199907112013",
                          'csrfmiddlewaretoken': "%s" % search('name=\'csrfmiddlewaretoken\'value=\'(.*?)\'', page).group(1), 'next': "/zh/"})
        self.headers.pop('referer')
        if not search('<a\shref="/zh/accounts/logout/">注销<', r.text):
            return False
        else:
            # 存储
            self.father.data['api'][self.name]['save_cookie'] = self.session.cookies.get_dict()
            self.father.dump_data('data')
            return True
