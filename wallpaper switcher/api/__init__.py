from random import shuffle, choice
from tool import write_img, dump_log


class BaseSpider(object):
    def __init__(self, father, name):
        self.father = father
        self.name = name
        self.img_set, self.img_idx = [], 0
        self.current_id, self.current_data = 0, []
        self.repeat = 0
        # 图标和所有分类
        self.b64_data = None
        self._cate = []
        self.interval, self.start = 1, 1
        self.down = False
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

    @property
    def cate(self):
        return self._cate

    @cate.setter
    def cate(self, cate):
        self._cate = cate
        if not self.father.data['api'][self.name].get('cate_page'):
            # 初始化页面数字
            self.father.data['api'][self.name]['cate_page'] = {}
            for c in self._cate[1:]:
                self.father.data['api'][self.name]['cate_page'][c] = self.start
            self.father.dump_data('data')


    #TODO ################# 自定义 ###################

    def a_page_spider(self, cate):
        """
        http request to get a page's images
        :param cate: category
        :return: r
        """
        raise NotImplementedError

    def a_page_finder(self, r, c):
        """
        process self.img_set
        :param r: response
        :param c: category
        :return: result
        """
        raise NotImplementedError

    def get_id_fromdata(self, data):
        """
        get image's id_ from data-list
        :param data: data-list
        :return: id_
        """
        raise NotImplementedError

    def a_img_spider(self, data):
        """
        http request to get image bytes and write it to file.find image's tail
        :param data: data-list
        :return: img, tail
        """
        raise NotImplementedError

    #TODO ################# 自定义 ###################

    def get_all_img(self):
        try:
            # 判断分类
            if self.father.config['category'] == '随机':
                cate = choice(list((set(self.cate[1:]) | set(self.father.data['api'][self.name]['ignore_list'])) - (
                            set(self.cate[1:]) & set(self.father.data['api'][self.name]['ignore_list']))))
            else:
                cate = self.father.config['category']
            # 爬虫下载
            r = self.a_page_spider(cate)
            self.repeat = 0
        except:
            if not self.father.switch_frame.abort and self.repeat <= 20:
                self.repeat += 1
                self.get_all_img()
            return
        # 爬虫正则
        result = self.a_page_finder(r, cate)
        self.img_idx = 0
        # 翻页操作
        if result and not self.down:
            if self.father.config['random_switch'] == '一页':
                shuffle(self.img_set)
            elif self.father.config['random_switch'] == '一类' and self.father.config['category'] == '随机':
                self.img_set = [choice(self.img_set)]
            self.father.data['api'][self.name]['cate_page'][cate] += self.interval
            dump_log(self.name + '--->' + str(cate) + ':翻页到='+str(self.father.data['api'][self.name]['cate_page'][cate]))
        else:
            self.father.data['api'][self.name]['cate_page'][cate] = self.start
            dump_log(self.name + '--->' + str(cate) + ':回到起始页='+str(self.start))
            if not self.down:
                self.get_all_img()
            else:
                self.down = False
        self.father.dump_data('data')

    def download_img(self):
        # 找到img_set有内容为止
        while not(self.img_set and len(self.img_set) > self.img_idx):
            self.get_all_img()
            self.repeat += 1
            if self.father.switch_frame.abort or self.repeat > 20:
                dump_log(self.name + '--->' + ':翻页中断/超时')
                return
        data = self.img_set[self.img_idx]
        self.img_idx += 1
        # 筛选: 不在黑名单
        id_ = self.get_id_fromdata(data)
        if id_ not in self.father.data["api"][self.name]['hate_list']:
            try:
                return_info = self.a_img_spider(data)
                if return_info == 'break':
                    self.father.set.api_choose.setEnabled(True)
                    self.father.set.api_choose.setCurrentText('随机')
                    if self.father.data['ignore_api'].count(self.name) == 0:
                        self.father.data['ignore_api'].append(self.name)
                        self.father.dump_data('data')
                    self.father.switch_frame.abort = True
                    dump_log(self.name + '--->' + ':登陆出错/网站拒绝')
                    return
                elif return_info:
                    img, tail = return_info
                else:
                    # 不符合条件
                    raise Exception
            except:
                if not self.father.switch_frame.abort and self.repeat <= 20:
                    self.repeat += 1
                    self.download_img()
                elif self.repeat == 20:
                    dump_log(self.name + '--->' + ':下载超时')
                    self.father.switch_frame.abort = True
                return
            # 缓冲区大小
            try:
                length = int(img.headers['Content-Length'])
            except KeyError:
                length = 102400
            length = 102400 if length <= 102400 else length
            # 传输正常且大小正常
            if not (img.ok and length / 1000 <= self.father.config['length'] and write_img(self, img, tail, length, id_, data) != 'small resolution'):
                self.download_img()
        else:
            self.download_img()

    def static_download(self):
        if not self.father.data['api'][self.name]['like_list']:
            return False
        else:
            data = choice(self.father.data['api'][self.name]['like_list'])[1]
            id_ = self.get_id_fromdata(data)
            try:
                return_info = self.a_img_spider(data)
                if return_info == 'break':
                    dump_log(self.name + '--->' + ':登陆出错/网站拒绝')
                    if self.father.data['ignore_api'].count(self.name) == 0:
                        self.father.data['ignore_api'].append(self.name)
                        self.father.dump_data('data')
                    self.father.switch_frame.abort = True
                    return False
                elif return_info:
                    img, tail = return_info
                else:
                    # 不符合条件
                    raise Exception
            except:
                if self.father.switch_frame.abort:
                    return True
                elif self.repeat == 20:
                    dump_log(self.name + '--->' + ':下载超时')
                    return False
                else:
                    self.repeat += 1
                    return self.static_download()
            try:
                length = int(img.headers['Content-Length'])
            except KeyError:
                length = 102400
            length = 102400 if length <=102400 else length
            # 传输正常
            if img.ok:
                # 写入到图片
                return write_img(self, img, tail, length, id_, data)
            else:
                return self.static_download()
