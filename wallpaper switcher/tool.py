from time import strftime, localtime
from win32api import RegOpenKeyEx, RegSetValueEx, RegDeleteValue, RegCloseKey
from win32con import HKEY_CURRENT_USER, KEY_SET_VALUE, REG_SZ, SPI_SETDESKWALLPAPER, HKEY_LOCAL_MACHINE
from win32gui import SystemParametersInfo
from os.path import dirname, getsize
from PIL.Image import open as im_open


def dump_log(s):
    if getsize('log.txt') >= 100000:
        open('log.txt', 'w').close()
    with open('log.txt', 'a', encoding='utf-8') as fp:
        fp.write(strftime('%Y-%m-%d %H:%M:%S', localtime()) + '\n\t')
        fp.write(s + '\n\n')

def set_wall(path=None):
    try:
        key = RegOpenKeyEx(HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, KEY_SET_VALUE)
        RegSetValueEx(key, 'WallpaperStyle', 0, REG_SZ, '2')
        RegSetValueEx(key, 'TileWallpaper', 0, REG_SZ, '0')
        if not path:
            path = dirname(__file__)+'/image/wall.jpg'
        SystemParametersInfo(SPI_SETDESKWALLPAPER, path, 1+2)
        RegCloseKey(key)
    except BaseException as e:
        dump_log('设置壁纸' + '--->' + str(e))

def write_img(obj, img, tail, length, id_, data):
    download_rate = 0
    with open('image/wall.' + tail, 'wb') as fp:
        try:
            for part in img.iter_content(length // 100):
                # 中断
                if obj.father.switch_frame.abort:
                    dump_log(obj.name + '--->' + ':(id='+str(id_)+')手动中断')
                    fp.close()
                    return False
                fp.write(part)
                download_rate += 1
                obj.father.switch_frame.process_signal.emit(-download_rate // 2)
        except BaseException as e:
            dump_log(obj.name + '--->'+str(e) + ':写入图片出错')
            obj.father.switch_frame.abort = True
            return False
        fp.close()
        try:
            im = im_open('image/wall.' + tail)
            if process_img(im, obj.father.resolving) == 'ERR':
                obj.father.switch_frame.white_label.move(0, 0)
                return 'small resolution'
            obj.father.last_api = obj.name
            obj.current_id, obj.current_data, obj.repeat = id_, data, 0
            return True
        except BaseException as e:
            dump_log('处理图片'+'--->'+str(e))
            obj.father.switch_frame.abort = True
            return False

def process_img(img, resolving):
    size = img.size
    multiply = min(size[0]/resolving[0], size[1]/resolving[1])
    if multiply < 1.0:
        # 分辨率过小
        return 'ERR'
    img = img.crop((int(size[0]/2 - resolving[0]*multiply/2), int(size[1]//2 - resolving[1]*multiply/2),
                    int(size[0]/2 + resolving[0] * multiply/2), int(size[1]//2 + resolving[1]*multiply/2)))
    img = img.convert('RGB')
    img.save('image/wall.jpg')
    return 'OK'

def auto_start(what, path):
    try:
        key = RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_SET_VALUE)
        if what:
            RegSetValueEx(key, 'MY_WINDMILL', 0, REG_SZ, '"%s" /start' % path)
        else:
            RegDeleteValue(key, 'MY_WINDMILL')
        RegCloseKey(key)
        return True
    except BaseException as e:
        dump_log('设置自启'+'--->'+str(e))
        return False

def try_author():
    try:
        key = RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_SET_VALUE)
        RegCloseKey(key)
        return True
    except:
        return False

