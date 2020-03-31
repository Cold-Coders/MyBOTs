import time
import uiautomator2
from util import *
import cv2


#其他操作
class Utils:
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
	def zoom_in(d):
		d.touch.down(255, 255) # 模拟按下

		d.drag(500, 255, 290, 255, 0.5)
		#time.sleep(.1) # down 和 move 之间的延迟，自己控制
		d.touch.up(255, 255) # 模拟抬起

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
