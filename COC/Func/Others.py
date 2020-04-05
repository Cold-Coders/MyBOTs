import time
import uiautomator2
import cv2
from util import *
from GUI.GUI_logs import *

#其他操作
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
		for elem in self.d.xpath("//android.widget.TextView").all():
			print("Text:", elem.text)
			# Dictionary eg: 
			# {'index': '1', 'text': '999+', 'resource-id': 'com.netease.cloudmusic:id/qb', 'package': 'com.netease.cloudmusic', 'content-desc': '', 'checkable': 'false', 'checked': 'false', 'clickable': 'false', 'enabled': 'true', 'focusable': 'false', 'focused': 'false','scrollable': 'false', 'long-clickable': 'false', 'password': 'false', 'selected': 'false', 'visible-to-user': 'true', 'bounds': '[661,1444][718,1478]'}
			print("Attrib:", elem.attrib)
			# Coordinate eg: (100, 200)
			print("Position:", elem.center())

	@staticmethod
	def save_screen(d,*args):
		if type(d) == uiautomator2.Device:
			screen = d.screenshot(format="opencv")
		else:
			screen = d
		n = len(args)
		if n == 1 and (type(args[0]) is int or type(args[0]) is str):
			cv2.imwrite(str(args[0]) + '.png', screen)
			return

		if n >= 1 and isinstance(args[0], AREA):
			screen = screen[args[0].y1:args[0].y2, args[0].x1:args[0].x2]
			if n >= 2 and args[1] == 'g':
				gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
				if n >= 3:
					cv2.imwrite('g_' + str(args[2]) + '.png', gray)  
				else:
					cv2.imwrite('g.png', gray)

		cv2.imwrite('screenshot.png', screen)

	@staticmethod
	def zoom_out(d):
		for i in range(r_num(lbound = 3)):
			d(className="android.view.View").pinch_in(percent=60, steps=10)
		show_log("Zoom_out")

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
				d.click(sx, sy)
			ss(random.randint(1,5) * 0.1)
		except(Exception):
			ss()
