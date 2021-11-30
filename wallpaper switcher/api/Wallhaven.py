from requests import get
from re import search, findall

from . import BaseSpider

class Wallhaven(BaseSpider):
    def __init__(self, father):
        super(Wallhaven, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB1dXVghYWFzJSTk/iam5v+np6e/6Kiov+kpKT/paWl/6Wlpf+lpaX/pKSk/6Ghof+enp7/mZmZ+oyMjNF1dXZgi4yMzZ2dnPOsrKz9tra2/7u7u/++vr7/wcHB/8LCwv/Dw8P/wsLC/8HBwf++vr7/ubm5/7CwsP6ioqL0kpKS0J2dnfqwsLD+ubm5/7+/v//ExMT/yMjI/8vLy//MzMz/zc3N/83Nzf/Ly8v/yMjI/8PDw/+9vr3/s7Oz/qKhofqlpaX/vLy8/7Kysv8vLy//TExM/8HBwf/T09P/1tbW/9bW1v8uLi7/TExM/5mZmf/MzMz/x8fH/8HBwf+qqqr/q6ur/8TExP/Jycn/z8/P/87Ozv93d3f/0dHR/97e3v/f39//SkpK/7e3t//X19f/09PT/87Ozv/Jycn/r6+v/7Kxsv/Kysr/z8/P/9XU1P/Z2dn/paWl/21tbf/l5uX/5ubm/3d3d/+Tk5P/3d3d/9nZ2f/U1NT/z8/P/7W1tf+2trb/z8/P/9TU1P/Z2dn/3t7e/97e3v8xMTH/5ubm/+3t7f+mpqb/aWlp/+Li4v/d3d3/2NjY/9PT0/+6urr/ubm5/9PT0//Y2Nj/3Nzc/2NjY//i4uL/SkpK/2VlZf+MjIz/gYGB/zk5Of/l5eX/4ODg/9zc3P/X19f/vb29/729vf/W1tb/29vb/9/f3/8lJSX/5OTk/4+Pj/+CgoL/8PDw/+7u7v8xMTH/0dHR/+Pj4//e3t7/2tra/8HBwf/BwcH/2dnZ/93d3f/h4eH/b29v/7+/v//Dw8P/T09P/+3t7f/s7Oz/Z2dn/5mZmf/k5OT/4ODg/93d3f/Dw8P/w8PD/9zc3P/f39//4uLi/+Dg4P+enp7/iYmJ/ycnJ//V1dX/6+vr/7CwsP9eXl7/5eXl/+Li4v/f39//x8bG/8bHxv/f4OD/4eHh/+Tk5P/m5ub/6ejo/+rq6v/r6+v/7Ozs/+vr6//p6un/ampq/8bGxf/k5OT/4eHh/8nJyf/Jycn+4eHh/+Tk5P/m5ub/6Ojo/+np6f/q6ur/6+vr/+vr6//r6+v/6urq/+Tk5P9qamr/TU1N/+Pj4//Ly8v+zc3N+N7e3v3l5eX/6Ojo/+np6f/q6ur/6+vr/+zs7P/s7Oz/7Ozs/+vr6//q6ur/6enq/+bm5v/g4OD9zs7P+NXV1szZ2dry4+Pj/erq6v/t7Oz/7Ozs/+3t7f/t7e3/7u7u/+3u7v/t7e3/7ezs/+vs6//l5eX+2trb89XV1c3e399e29zczNfX1/jW1tb+19fX/9fX1//Y2Nj/2NjY/9jY2P/Y2Nj/2NjY/9fX1//X19f/2NjY+tva2s7f399ggAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAEAAA=='
        self.cate = ['随机', 'Animals', 'Architecture', 'Cities', 'Food', 'Forest', 'Landscapes', 'Literature', 'Movies', 'Music', 'Mountain', 'Nature', 'Plants', 'Scenery', 'Sea', 'Sky', 'Sports', 'Transportation']

    def a_page_spider(self, cate):
        return ''.join(get('https://wallhaven.cc/search?q=%s&atleast=%sx%s&page=%s' % (cate.lower(), self.father.resolving[0], self.father.resolving[1], self.father.data['api'][self.name]['cate_page'][cate]), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall('data-wallpaper-id="(.{2})(.*?)"', r)
        new_set = [[''.join(x), 'https://w.wallhaven.cc/full/%s/wallhaven-%s.jpg' % (x[0], ''.join(x))] for x in new_set]
        result = True if (new_set != self.img_set) and new_set else False
        self.img_set = new_set
        return result

    def get_id_fromdata(self, data):
        return data[0]

    def a_img_spider(self, data):
        id_, url = data
        img = get(url, stream=True, timeout=self.father.config['timeout'], headers=self.headers)
        tail = search('.*?([jpnegJPENG]{3,4})$', img.headers['Content-Type']).group(1)
        return img, tail
