import pyzbar.pyzbar as zbar
import cv2 as cv
from tkinter.filedialog import askopenfilename
from tkinter import Tk

def do_from_img():
    tk = Tk()
    tk.withdraw()
    s = askopenfilename(master=tk, title='选择图片', filetypes=[('All Image', '*.*')])
    img = cv.imread(s)
    if img is not None:
        read_re = read_qr(img)
        if read_re:
            return [img, read_re]
    return None


def do_from_camera():
    cv.namedWindow('read')
    cpt = cv.VideoCapture(0)
    read_re = None
    while cpt.isOpened():
        ok, frame = cpt.read()
        if not ok:
            return None

        read_re = read_qr(frame)
        if read_re:
            read_re = [frame, read_re]
            cv.imshow('read', frame)
            cv.waitKey(200)
            break

        cv.imshow('read', frame)
        key = cv.waitKey(50 // 3)
        if cv.getWindowProperty('read', cv.WND_PROP_AUTOSIZE) < 1 or key == 27:
            break
    cpt.release()
    cv.destroyAllWindows()
    return read_re


def read_qr(img):
    codes = zbar.decode(img)
    lis = []
    if codes:
        idx = 1
        for code in codes:
            polygon = code.polygon
            cv.line(img, (polygon[0].x, polygon[0].y), (polygon[1].x, polygon[1].y), (255, 0, 0), 3)
            cv.line(img, (polygon[1].x, polygon[1].y), (polygon[2].x, polygon[2].y), (255, 0, 0), 3)
            cv.line(img, (polygon[2].x, polygon[2].y), (polygon[3].x, polygon[3].y), (255, 0, 0), 3)
            cv.line(img, (polygon[0].x, polygon[0].y), (polygon[3].x, polygon[3].y), (255, 0, 0), 3)
            cv.circle(img, (polygon[0].x, polygon[0].y), 25, (0, 0, 255), -1)
            cv.putText(img, str(idx), (polygon[0].x-12, polygon[0].y+12), cv.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 4)
            lis.append(code.data.decode())
            idx += 1
    return lis
