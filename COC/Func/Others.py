import time, cv2, os.path ,sys
import aircv as ac
import uiautomator2
import numpy
import pytesseract

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
	def find_position(d,target,confidence = 0.8):
		if type(d) is uiautomator2.Device:
			imsrc = d.screenshot(format="opencv")
		elif type(d) is numpy.ndarray:
			imsrc = d
		else:
			Utils.prt("Error (uiautomator2)",mode = 4)
			return

		if not os.path.isfile(target):
			Utils.prt("Error by Reading Image",mode = 4)
			return

		imobj = ac.imread(target)
		
		result = ac.find_template(imsrc, imobj)

		if result['confidence'] > confidence:
			pos = (int(result['result'][0]),int(result['result'][1]))
		else:
			print(result)
			pos = (-1,-1)
		return pos


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
	def save_screen(d,gray = False,*args):
		if type(d) == uiautomator2.Device:
			screen = d.screenshot(format="opencv")
		else:
			screen = d

		n = len(args)

		#if gray is enable, make it as gray
		if gray:
			screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

		if n == 1 and (type(args[0]) is int or type(args[0]) is str):
			cv2.imwrite(str(args[0]) + '.png', screen)
			return

		count = 1
		filename = 'screenshot'
		while os.path.isfile(filename + str(count) + ".png"):
			count += 1

		cv2.imwrite(filename + str(count) + ".png" , screen)

		gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
		cv2.imwrite(filename + str(count) + "_g.png" , gray)

		Utils.prt("Screenshot saved. file: " + filename + str(count) + ".png",mode = 2)
		

	@staticmethod
	def zoom_out(d):
		for i in range(r_num(lbound = 3)):
			d(className= VIEWVIEW).pinch_in(percent=60, steps=10)
		Utils.prt("Zoom_out",mode = 2)

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
				d.click(random.randint(1,sx), random.randint(1,sy))
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
		x1,y1,x2,y2 = area

		cropped = screen[y1:y2, x1:x2]

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
			print("error")
		

	'''
	Orc by tesseract
	'''
	@staticmethod
	def orcbyArea(screen,area):
		x1,y1,x2,y2 = area

		cropped = screen[y1:y2, x1:x2]
		cv2.imwrite('cropped.jpg', cropped)
		
		gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
		cv2.imwrite("cropped.png", gray) 

		#Image.open("cropped.png")
		#Image.fromarray(gray)
		tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
		if sys.platform == 'win32':
			text = pytesseract.image_to_string(Image.fromarray(gray), config=tessdata_dir_config , lang='chi_sim')
		else:
			text = pytesseract.image_to_string(Image.fromarray(gray), lang='chi_sim')
		
		#os.remove("cropped.png")

		print("tesseract :", text)
		return text