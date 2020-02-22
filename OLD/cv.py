import imutils,cv2,numpy as np
import pytesseract
import uiautomator2

from matplotlib import pyplot as plt
from util import *
from Orc import *
from PIL import Image
from aip import AipOcr

WIN10 = True
tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
aipOcr  = AipOcr(APP_ID, API_KEY, SECRET_KEY)

class CV:

    @staticmethod
    def Save(d,*args):
        if type(d) == uiautomator2.Device:
            screen = d.screenshot(format="opencv")
        else:
            screen = d
        n = len(args)
        if n == 1 and (type(args[0]) is int or type(args[0]) is str):
            cv2.imwrite('s' + str(args[0]) + '.png', screen)
            return

        if n >= 1 and isinstance(args[0], AREA):
            screen = screen[args[0].y1:args[0].y2, args[0].x1:args[0].x2]
            if n >= 2 and args[1] == 'g':
                gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
                if n >= 3:
                    cv2.imwrite('g' + str(args[2]) + '.png', gray)  
                else:
                    cv2.imwrite('g.png', gray)

        cv2.imwrite('s.png', screen)


    @staticmethod
    def Crop(img, rel_pos, edge=46,scale=1):
        #截取rel_pos附近一个小方块
        if len(rel_pos) == 2:
            rx,ry = rel_pos
            h=len(img)
            w=len(img[0])

            x0 = int(rx*w - edge*scale)
            x1 = int(rx*w + edge*scale)
            y0 = int(ry*h - edge*scale)
            y1 = int(ry*h + edge*scale)
            return img[y0:y1,x0:x1]#print("Edges",edge*scale)
        else:#截取特定区域y1:y2,x1:x2
            #print(rel_pos[0],rel_pos[1],rel_pos[2],rel_pos[3])
            return img[rel_pos[1]:rel_pos[3],rel_pos[0]:rel_pos[2]]


    @staticmethod
    def find(img_rgb : np.ndarray,target,d = False):
        #img_rgb = cv2.imread('mario.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(target,0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)

        p = list()

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            p.append(( int(pt[0] + w/2) , int(pt[1] + h/2) ))

        if d:
            cv2.imwrite('res.png',img_rgb)
            
        if len(p) > 0:
            return p
        return None

    @staticmethod
    def Match(img_rgb : np.ndarray,target,criteria = 0.9,d = False):
        #img_rgb = cv2.imread('mario.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(target,0)
        w, h = template.shape[::-1]

        # Apply template Matching
        method = cv2.TM_SQDIFF_NORMED
        res = cv2.matchTemplate(img_gray,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        

        val = 1 - min_val
        if val < criteria:
            if d:
                print("未找到",target,"criteria:",val,"< (",criteria,")")
            return (-1,-1)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        if d:
            print(target,"criteria:",val,"(",criteria,")")
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(img_rgb,top_left, bottom_right, 255, 2)
            cv2.imwrite('res.png',img_rgb)
        #plt.subplot(121),plt.imshow(res,cmap = 'gray')
        #plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        #plt.subplot(122),plt.imshow(img_rgb,cmap = 'gray')
        #plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        #plt.suptitle(method)

        #plt.show()
        return ( int(top_left[0] + w/2) , int(top_left[1] + h/2) )

    """
    获取某一坐标的RGB值(灰度图会报错)
    """
    @staticmethod
    def getPixel(img, rx, ry):
        pixel = []
        if type(rx) is float and type(ry) is float:
            pixel = img[int(ry*len(img)), int(rx*len(img[0]))]
        else:
            pixel = img[int(ry), int(rx)]
        return pixel[2],pixel[1],pixel[0]

    '''
    Baidu Orc
    '''
    @staticmethod
    def BdOrc(cropped,Accurate = False):
        # 定义参数变量
        options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
        "detect_language" : "true",
        "probability" : "false"
        }

        #cropped = screen[area[1]:area[3], area[0]:area[2]]

        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("cropped.png", gray)

        # 调用通用文字识别接口
        result = aipOcr.basicGeneral(get_file_content("cropped.png"), options) if not Accurate else aipOcr.basicAccurate(get_file_content("cropped.png"), options)
        result = result["words_result"]
        if type(result) is list and len(result) > 0:
            result = result[0]["words"]

            os.remove("cropped.png")
            return result
