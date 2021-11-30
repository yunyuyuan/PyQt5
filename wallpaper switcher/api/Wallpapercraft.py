from requests import get
from re import search, findall, sub

from . import BaseSpider

class Wallpapercraft(BaseSpider):
    def __init__(self, father):
        super(Wallpapercraft, self).__init__(father, self.__class__.__name__)

        self.b64_data = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAFRUlEQVR4nK2XeWwUZRTAf9/M7G63uy1tEQpbIBwBEcUgiMQzKgGRVgLBcIhB5VIMCXJpJMipIYox/qNQwSA0RAQiV4vcSEAUOYIcCZEjymFbS++lx+7MPP/YZdulpZ1W3n8z8773ft/73vfeG0UrRPYSIMQ2S9RAXZNqFHM4TrZagt0ae84d78Ijuay0dmFtW5wkXbv2lLFDMqR8iy6SxyXZyRMttakcOd6Em0TGisb6Czc8DFvWhcoaLbY4bCkWjC7ivaxSvC77DDYjVRZ/3xcA2cpTJLC2JKj3mp7dkdzTfly6NNQDUrw2X0/LJ3NAULBYQxWz1RiCrQKQ7aTjYncI1e/jH9rx+Y403EZDxw3WCaT5LPI+ukbvjJCl2Uwnne/U44QdAcg+2lDDUtvNjM1HkrX3c9Ipu62hHB1WnYRCGqMGVfDZpEIyks3LCO+qTPbdE0AWoTGQ19BYdaXQ7Xv5k84UlBpoWsscx20GMEOKxeOLmPlKCW7kCGHGqZH80xAgjyv5QaP7jOwO7Drlx+NuPtyOQQSSvTZfTipg9KBKEKapTFbHAVRt1SQwpRei3T/Hd4ttK+ZmFrNwbNFNlUknAOPOR8sGE0Gvv0DAMusO3+WSOGOW1fC9ZSnsaDlSgFHvm6YJNZYCIfYyBtCYPNIpxJaF18EEEqD3Wz1iOTFlcClzXy3GDCv6zeqOLZFQzx9TxBsvlgNw5loCY5dnoDeRR02m2OVCF15DCPhMAm6TBwMhIOJo5vASAj6TzilhHsqoBSIFafqQ0oi+32TPbz60Zm5PkwC3azTOX/JEHiwY3j+ILeDShc5tI9daAZMHlwGQ4rNIbhOJv63DvrP+Zq9vkwCGIaz/uU0sVSe8WI4IZA6oRKuXLGOerCBkKnoHatEiwaDWVFwtcDftvTkABew85YdoEAJpJolu4cNRxVDvsvi9Nv4Em3FPV8Te7T7px+Vqvjk2W2ZKgga3bkW263fZdE8P0aPjXVVVYN6IYgY+XBN5NmD9oTZNJp9jgESPzf6zvkg4bPjm7XyMaK0oqqi7RBOeqaBP+2gyhhWHzvma9+4EAGDN/tSIpkDfLrWoaPjn5bSP6QTSwniiXfLPQjeWs07vDOCPax7Kq+NVRcGB8z42HE2OV1aw9ZckNOWsojoCqKrRuHwzPqN/veSlsloj53BKXE+1gZ0nkhx3T0cAhi5sPha/03UHUgD4/XJCXHSCYY1z1xOceXcKoBRsO5kErsiziSL3tB8AWxRHLybGdE9c9KJpzmfTuF5ghRW6p/Gz+6vAxeGzibh0oSSkc7u2jn3ppgdI9VmgYOWeVAy9UROIgCaAqju0unkgl3+vlbnajVmRwbnrCY3OfeFoZ1QqciyNfdN1aVD/BTA0WP56IVMHl6FsFqkslsYDHMJPFR/YGgv2nvYxZVWAYM3/GIeiUl2rMfG5cj6dVEiax7qIxUQ1ghMNIhAD2UYSBhtsg8zs3anagu/bY9oO5/d6YpmKx7rVsG7WTbq1CxdhMlVlsf1uvXtPxT/RH8gprdb7zP42nY1Hkx2NaSKQ5LXJfief4f2DKJsVGCxRL3G7Mf3m/wt2MRSNjQUlRuqwZV24WuRqtMdL1NhXU/IZ92yF6MJBwoxSI6lsyr6zP6NjeClmvugsyDvtZ8bqDpRV1aV62FK8+XwZy8YXkZZoXUCYrLI47sR2i0R+pK3kcTC0Q9mr56RIWnovebRPd7mRY4jkUik7GCqLnNWWO9LS3IqA5DIAWBuyVF/DEEuDL0hkvnoBs6W2WgUAIJvQSaAnXvLVEMpba+c/Crr8lIdLU+8AAAAASUVORK5CYII='
        self.cate = ['随机', 'Animals', 'Abstract', 'City', 'Food', 'Forest', 'Landscapes', 'Movies', 'Fantasy', 'Mountain', 'Nature', 'Space', 'Scenery', 'Music', 'Sky', 'Sports']

    def a_page_spider(self, cate):
        return ''.join(get('https://wallpaperscraft.com/search/?page=%s&query=%s&size=%sx%s' % (self.father.data['api'][self.name]['cate_page'][cate], cate.lower(), self.father.resolving[0], self.father.resolving[1]), headers=self.headers, timeout=self.father.config['timeout']).text.split())

    def a_page_finder(self, r, c):
        new_set = findall(r'<spanclass="wallpapers__canvas"><imgclass="wallpapers__image"src="(.*?)"', r)
        new_set = [[search('_(\d*)_\d*x\d*', x).group(1), sub('\d*x\d*', str(self.father.resolving[0])+'x'+str(self.father.resolving[1]), x)] for x in new_set]
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
