# 桌面壁纸一键切换<img src="https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/image/main.ico?raw=true" width="50" height="50" alt="图片加载失败时，显示这段字"/>


 * [下载包含exe可执行文件的rar](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/wallpaper_switcher.rar?raw=true)
---
#### 更新
>1.新增4个网站,新增cookie登陆,pixabay和ssyer需要自己的账号,在TODO位置\
2.新增日志文件,错误或信息将写到log.txt\
3.注:ssyer的cookie失效后需要手动输入验证码登陆.pixabay连续下载多个图片会被ban一会.Hdwallpaper偶尔会抽风显示水印
#### 说明
> 原本写了5个网站的,上面的壁纸基本用一辈子都用不完\
后来实在闲的蛋疼,到处找壁纸网站写api,写了10个左右就干脆弄了个BaseSpider做基本工作\
后面陆续整理了共~~20~~25个网站\
虽然程序一般般,你可以随便转载并标明是自己写的,我无所谓\
_**但,请勿商用！！！**_
## 文件目录
 **Wallpaper Switcher**
* [**api**](https://github.com/yunyuyuan/invoker/tree/master/pyqt/wallpaper%20switcher/api)-------------------------------(爬虫接口)
	* [**\_\_init__**.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/__init__.py) (BaseSpider)
	* [**LocalWallpaper_**.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/LocalWallpaper_.py) (Local)
	* [Alphacoders.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Alphacoders.py)
	* [Baidu.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Baidu.py)
	* [Bestwallpaper.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Bestwallpaper.py)
	* [Bing.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Bing.py)
	* [Desktopwallpaper.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Desktopwallpaper.py)
	* [Hddesktop.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Hddesktop.py)
	* [Pexels.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Pexels.py)
	* [Pixabay.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Pixabay.py)
	* [Sogou.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Sogou.py)
	* [Unsplash.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Unsplash.py)
	* [Wallhaven.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Wallhaven.py)
	* [Wallpapercave.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Wallpapercave.py)
	* [Wallpapercraft.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Wallpapercraft.py)
	* [Wallpaperhi.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Wallpaperhi.py)
	* [Wallpaperhome.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Wallpaperhome.py)
	* [Wallpapersite.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Wallpapersite.py)
	* [Wallpapertag.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Wallpapertag.py)
	* [Wallpaperup.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Wallpaperup.py)
	* [Wallpaperwide.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Wallpaperwide.py)
	* [Zol.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Zol.py)
	* [Hdwallpaper.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Hdwallpaper.py)
	* [Huyanbizhi.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Huyanbizhi.py)
	* [V3wall.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/V3wall.py)
	* [Ssyer.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Ssyer.py)
    * [Visualhunt.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/api/Visualhunt.py)
	* 以后会更多......
* [**frames**](https://github.com/yunyuyuan/invoker/tree/master/pyqt/wallpaper%20switcher/frames)--------------------------(PyQt窗口)
	* [switch_frame.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/frames/switch_frame.py)---------(风车-点击切换)
	* [choose_random.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/frames/switch_frame.py)------(随机壁纸选项)
	* [set.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/frames/set.py)---------------------(设置界面)
	* [right_frame.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/frames/right_frame.py)-----------(收藏 | 黑名单)
	* [verify.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/frames/verify.py)-----------(输入验证码)
* [**image**](https://github.com/yunyuyuan/invoker/tree/master/pyqt/wallpaper%20switcher/image)
	 * 图片资源
* [config.json](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/config.json)----------------------(配置文件)
* [data.json](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/data.json)------------------------(数据文件)
* [style.qss](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/style.qss)-------------------------(样式文件)
* [tool.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/tool.py)---------------------------(工具函数)
* [tray.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/tray.py)---------------------------(托盘类)
* [main.py](https://github.com/yunyuyuan/invoker/blob/master/pyqt/wallpaper%20switcher/main.py)--------------------------(主程序)
---
## 自定义接口-继承BaseSpider
#### \_\_init\_\_.py
```python
from random import shuffle, choice
from tool import write_img


class BaseSpider(object):
    """基类"""
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

    #TODO ################# 自定义 ###################

    def a_page_spider(self, cate):
        """
        http request to get one page's images
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
        http request to get image bytes and find image's tail
        :param data: data-list
        :return: img, tail
        """
        raise NotImplementedError

    #TODO ################# 自定义 ###################

    def get_all_img(self):
        """
        get all image's url from one page
        """
        pass

    def download_img(self):
        """
        download a image
        """
        pass

    def static_download(self):
        """
        download a image from like_list
        """
        pass

```

#### 一个子类爬虫看起来是这样的
```python
from requests import get
from urllib.request import quote
from re import search, findall

from . import BaseSpider

class Baidu(BaseSpider):
    """ 百度 """
    def __init__(self, father):
        super(Baidu, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'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'
        self.cate = ['随机', '风景', '雪景', '宇宙', '山水', '夜景', '蓝天', '秋天', '田园', '星空', '自然', '冰雪', '唯美', '可爱', '小清新', '插画', '水墨画', '个性', '简约', '护眼', '节日', '中国风', '炫酷', '3D', '科幻', '时尚', '星座', '古典', '淡雅', '创意设计', '美食', '三维立体', '高清壁纸', '萌宠', '卡通', '体育', '国家地理', '手绘素描', '旅游风光', '治愈系', '卡通动漫', '游戏动漫', '动物', '影视', '游戏', '花草', '明星', '跑车']
        self.interval, self.start = 30, 0

    def a_page_spider(self, cate):
        return ''.join(get('https://image.baidu.com/search/index?tn=baiduimage&word=%s+%s&pn=%s' % ('%E5%A3%81%E7%BA%B8', quote(cate), self.father.data['api'][self.name]['cate_page'][cate]), timeout=self.father.config['timeout']).content.decode().split())

    def a_page_finder(self, r, c):
        new_set = findall(r'"pageNum":.*?,"objURL":"(.*?)","fromURL":.*?"width":(\d*),"height":(\d*).*?"di":"(\d*)"', r)
        empty = False if new_set else True
        new_set = [[x[0], x[3]] for x in new_set if int(x[1]) >= self.father.resolving[0] and int(x[2]) >= self.father.resolving[1]]
        result = True if (new_set != self.img_set) and not empty else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[1]

    def a_img_spider(self, data):
        url, id_ = data
        img = get(url, stream=True, timeout=self.father.config['timeout'])
        tail = search('.*?/([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail

```