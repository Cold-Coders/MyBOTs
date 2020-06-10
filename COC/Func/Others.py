import time, cv2, os.path ,sys
import aircv as ac
import uiautomator2
import numpy as np
import pytesseract
import imutils

from aip import AipOcr
from PIL import Image

from GUI.GUI_logs import *
from CONSTANT import *
from util import *
from Orc import *


aipOcr  = AipOcr(APP_ID, API_KEY, SECRET_KEY)

class Utils:

	@staticmethod
	def prt(*args,mode = 1):
		n = len(args)
		for i in range(n):
			if type(args[i]) is str or type(args[i]) is int:
				show_log(args[i],mode = mode)

			elif type(args[i]) is list:
				for sub_msg in args[i]:
					if type(sub_msg) is str:
						show_log(sub_msg, mode = mode)
					else:
						show_log(str (type(sub_msg)) + " is not support by prt" ,mode = 2)

			elif type(args[i]) is dict:
				for key in args[i].keys():
					show_log( str(key) + " : " + str(args[i][key]) ,mode = mode)

	@staticmethod
	def getElementByTextview(d):
		# get all text-view text, attrib and center point
		for elem in self.d.xpath("//" + TEXTVIEW).all():
			print("Text:", elem.text)
			# Dictionary eg: 
			# {'index': '1', 'text': '999+', 'resource-id': 'com.netease.cloudmusic:id/qb', 'package': 'com.netease.cloudmusic', 'content-desc': '', 'checkable': 'false', 'checked': 'false', 'clickable': 'false', 'enabled': 'true', 'focusable': 'false', 'focused': 'false','scrollable': 'false', 'long-clickable': 'false', 'password': 'false', 'selected': 'false', 'visible-to-user': 'true', 'bounds': '[661,1444][718,1478]'}
			print("Attrib:", elem.attrib)
			# Coordinate eg: (100, 200)
			print("Position:", elem.center())

	@staticmethod
	def test_read_img(d,target):

		def draw_circle(img, pos, circle_radius, color, line_width):
			cv2.circle(img, pos, circle_radius, color, line_width)
			cv2.imshow('objDetect', imsrc) 
			cv2.waitKey(0)
			cv2.destroyAllWindows()

		imsrc = d.screenshot(format="opencv")
		circle_center_pos = Utils.find_position(imsrc,target)
		Utils.prt("position: " + str(circle_center_pos) ,mode = 0)
		circle_radius = 20
		color = (0, 0, 255)
		line_width = 2
		
		draw_circle(imsrc, circle_center_pos, circle_radius, color, line_width)

	# save_screen(d) - one file as screenshot.png
	# save_scree(d, filename )  save screenshot as filename
	@staticmethod
	def save_screen(d,*args,gray = False):
		if type(d) == uiautomator2.Device:
			screen = d.screenshot(format="opencv")
		else:
			screen = d

		n = len(args)

		filename = 'screenshot'
		
		if n == 1 and (type(args[0]) is int or type(args[0]) is str):
			cv2.imwrite(str(args[0]) + '.png', screen)
			return

		#if gray is enable, make it as gray
		if gray:
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
			filename = "screenshot_g"

		count = 1
		while os.path.isfile(filename + str(count) + ".png"):
			count += 1

		cv2.imwrite(filename + str(count) + ".png" , screen)

		#gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
		#cv2.imwrite(filename + "_g" + str(count) + ".png" , gray)

		Utils.prt("Screenshot saved. file: " + filename + str(count) + ".png",mode = 2)
		

	@staticmethod
	def zoom_out(d,lower = 1,upper = 2,percent = 60, steps = 10):
		try:
			for i in range(r_num(lbound = lower,ubound = upper)):
				d(className= VIEWVIEW).pinch_in(percent = percent, steps = steps)
			Utils.prt("Zoom_out",mode = 2)
		
		except Exception as e:
			#raise e
			xml = d.dump_hierarchy()
			prt(xml)
	
	@staticmethod
	def msg(d,msg,prt = True, mode = 1, times = 1):
		d.toast.show(msg, times)
		if prt:
			Utils.prt(msg,mode = mode)

	@staticmethod
	def current_app(d):
		return d.app_current()['package']

	@staticmethod
	def current_act(d):
		return d.app_current()['activity']

	@staticmethod
	def tap(d,sx,sy,r = False):
		try:
			if r:
				d.click(random.randint(sx,sy), random.randint(sx,sy))
			else:
				d.click(sx +r_num(lbound = 3), sy + r_num(lbound = 3))
			ss(random.randint(1,5) * 0.1)
		except(Exception):
			ss()

	'''
	Baidu Orc
	'''
	@staticmethod
	def BdOrc(screen,area,Accurate = False):
		# 定义参数变量
		options = {
		  'detect_direction': 'true',
		  'language_type': 'CHN_ENG',
		  "detect_language" : "true",
		  "probability" : "false"
		}

		#x1,y1,x2,y2 = area
		#cropped = screen[y1:y2, x1:x2]
		cropped = Utils.crop_screen(screen,area)

		gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
		
		cv2.imwrite("cropped.png", gray)

		def get_file_content(filePath):
			with open(filePath, 'rb') as fp:
				return fp.read()

		# 调用通用文字识别接口 get_file_content("cropped.png")
		result = aipOcr.basicGeneral(get_file_content("cropped.png"), options) if not Accurate else aipOcr.basicAccurate(get_file_content("cropped.png"), options)
		
		os.remove("cropped.png")

		print(result)

		if "words_result" in result:
			result = result["words_result"]
			if type(result) is list and len(result) > 0:
				result = result[0]["words"]
			return result
		else:
			print("baidu orc error")
		
	@staticmethod
	def revert_test():
		count = 1
		filename = 'screenshot'
		while os.path.isfile(filename + str(count) + ".png"):
			img = cv2.imread(filename + str(count) + ".png")
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			cv2.imwrite(filename + str(count) + ".tif" ,Utils.revert_white_to_black(gray) )
			Utils.prt("已将" + filename + str(count) + "处理为ORC图片",mode = 4)
			count += 1

	@staticmethod
	def revert_white_to_black(gray):
		h = gray.shape[0]
		w = gray.shape[1]
		dst = np.zeros((h,w),np.uint8)

		for i in range(0,h):
			for j in range(0,w):
				if gray[i,j] > 250:
					dst[i,j] =  0
				else:
					dst[i,j] = 255

		#if False:		
		#	count = 1
		#	while os.path.isfile('cropped' + str(count) + ".tif"):
		#		count += 1
		#	cv2.imwrite('cropped' + str(count) + ".tif", dst)

		return dst

	@staticmethod
	def test_crop(d,area):
		imsrc = Utils.crop_screen(d.screenshot(format="opencv"),area)
		cv2.imshow('Crop test', imsrc) 
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	@staticmethod
	def crop_screen(screen,area):
		if type(screen) == uiautomator2.Device:
			screen = screen.screenshot(format="opencv")
		else:
			screen = screen
		x1,y1,x2,y2 = area
		return screen[y1:y2, x1:x2]

	'''
	Orc by tesseract
	'''
	@staticmethod
	def orcbyArea(screen,area,lang = "num", Debug = False):
		#x1,y1,x2,y2 = area
		#cropped = screen[y1:y2, x1:x2]
		cropped = Utils.crop_screen(screen,area)
		#cv2.imwrite('cropped.png', cropped)
		
		gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

		revert = Utils.revert_white_to_black(gray)
		recogize = Image.fromarray(revert)
		
		#Image.open("cropped2.png")
		#Image.fromarray(gray)
		#tessdata_dir_config = '--tessdata-dir "C:/Program Files/Tesseract-OCR/tessdata"'
		tessdata_dir_config = '--tessdata-dir "Tesseract_font/"'

		if sys.platform == 'win32':
			text = pytesseract.image_to_string(recogize, config=tessdata_dir_config , lang=lang)
		else:
			text = pytesseract.image_to_string(recogize, lang=lang)
		
		#os.remove("cropped.png")
		count = 1
		if Debug:
			while os.path.isfile('cropped' + str(count) + ".tif"):
				count += 1
			cv2.imwrite('cropped' + str(count) + ".tif", revert)
			print("tesseract:", text)
		return text

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

	@staticmethod
	def r_color(c1,c2,diff = 8, Debug = False):
		is_color = False
		if type(c1) is tuple and type(c2) is tuple :
		  is_color = abs(c1[0] - c2[0]) <= diff and abs(c1[1] - c2[1])  <= diff and abs(c1[1] - c2[1]) <= diff
		elif type(c1) is int and type(c2) is int:
		  is_color = abs(c1 - c2) <= diff
		elif len(c1) == 3 and len(c2) == 3:
		  is_color = abs(c1[0] - c2[0]) <= diff and abs(c1[1] - c2[1])  <= diff and abs(c1[1] - c2[1]) <= diff
		if not is_color and Debug:
			print("Color1 ", c1, "Color2 ", c2 )
		return is_color

	@staticmethod
	def isColor(screen,pos,color,diff = 8, Debug = False):
		if type(screen) == uiautomator2.Device:
			screen = screen.screenshot(format="opencv")
		else:
			screen = screen
		x,y = pos
		pixel = Utils.getPixel(screen,x,y)
		return Utils.r_color(pixel,color,diff, Debug)

	@staticmethod
	def find_position(d,target,confidence = 0.7, Debug = False):
		if type(d) is uiautomator2.Device:
			imsrc = d.screenshot(format="opencv")
		elif type(d) is np.ndarray:
			imsrc = d
		else:
			Utils.prt("Error (uiautomator2)",mode = 4)
			return

		#print(target, type(target))
		if type(target) is np.ndarray:
			imobj = target
		elif not os.path.isfile(target):
			Utils.prt("Error by Reading Image",mode = 4)
			return
		else:
			imobj = ac.imread(target)
		
		result = ac.find_template(imsrc, imobj)
		if result is None:
			return (-1,-1)

		if result['confidence'] > confidence:
			print ('找到', target,'阈值:' , result['confidence'])
			return (int(result['result'][0]),int(result['result'][1]))
			
		if Debug:
			print(result)

		return (-1,-1)

	@staticmethod
	def find_PosbyArea(d,Area,target,confidence = 0.7,Debug = False ):
		if type(d) is uiautomator2.Device:
			imsrc = d.screenshot(format="opencv")
		elif type(d) is np.ndarray:
			imsrc = d
		else:
			Utils.prt("Error (uiautomator2)",mode = 4)
			return
		imsrc = Utils.crop_screen(imsrc,Area)
		return Utils.find_position(imsrc,target,confidence,Debug = Debug)


	@staticmethod
	def Image_Test(d, upper = [],lower = [], morph = 3):
		if morph == "":
			morph = 1
		elif not morph.isdigit():
			return 
		morph = int(morph)

		if type(upper) is not list or type(lower) is not list:
			return
		elif upper == [''] or len(lower) == ['']:
			upper = [77, 165 , 145]
			lower = [70, 120 , 45]
		else:
			try:
				upper = [int(i) for i in upper]
				lower = [int(i) for i in lower]
			except Exception as e:
				raise e


		def getposHsv(event,x,y,flags,param):
			if event==cv2.EVENT_LBUTTONDOWN:
				print("(",x,",",y,")","HSV is",hsv[y,x])

		def getposBgr(event,x,y,flags,param):
			if event==cv2.EVENT_LBUTTONDOWN:
				print("Bgr is",screen[y,x])

		# 增加判断screen，也就是截图是否成功的判断
		screen = d.screenshot(format="opencv")
		if screen.size:

			hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV);

			#print(hsv[325][271]) #(325,271)
			lower_hsv = np.array(lower)#[57, 43, 46]
			high_hsv = np.array(upper) #[67, 255, 255]

			img = cv2.inRange(hsv, lowerb = lower_hsv, upperb = high_hsv)
			kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (morph, morph))
			img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
			dstPoints = []
			#cv2.circle(img, (325, 271), 1, (255, 255, 255), 1)
			#h = screen.shape[0]
			#w = screen.shape[1]
			#for i in range(0,h):
			#	for j in range(0,w):
			#		pixel = screen[i, j]
			##		black = np.array([0,0,0])
			#		white = np.array([255,255,255])
			#		R = pixel[2]
			#		G = pixel[1]
			#		B = pixel[0]
			#		if R == 61 and G == 121 and B == 181:
			#			screen[i,j] = white
			#			continue
			#		screen[i,j] = black
					#print(pixel,type(pixel))
			
			#img2 = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

			cv2.imshow("Green", img)
			cv2.imshow("Origin", hsv)
			cv2.setMouseCallback("Origin",getposHsv)
			cv2.waitKey(0)
			# 找轮廓
			cnts = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			cnts = cnts[1] if imutils.is_cv3() else cnts[0]

			if len(cnts):
				for c in cnts:
					# 获取中心点
					M = cv2.moments(c)
					if M["m00"] == 0:
						continue
					#print(M)
					cX = int(M["m10"] / M["m00"])
					cY = int(M["m01"] / M["m00"])
					#
					dstPoints.append((cX,cY))

					# 画出轮廓和中点
					cv2.drawContours(screen, [c], -1, (0, 255, 0), 2)
					cv2.circle(screen, (cX, cY), 20, (0, 0, 255), 1)
					cv2.putText(screen, "center", (cX - 20, cY - 20),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				cv2.imshow("inRange2", screen)
				cv2.waitKey(0)
			#return dstPoints
		else:
			raise Exception('Screen process is unsuccessful')