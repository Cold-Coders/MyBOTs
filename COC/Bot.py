import uiautomator2 as u2
import threading
from util import *
from Constant import *
from COC.Func.Others import *



class COC_BOT:

	def __init__(self,device = "",config = {}):
		self._error = 0

		self.d = u2.connect(device)
		prt(self.d.info,title = "机器信息")

		self._util = Utils()
		self._app = self._util.current_app(self.d)

		if self._app not in GameList:
			self._error = 1
			return

		self._config = config
		self._count = dict()

	def run(self):
		if self._error == 1:
			msg("请在游戏界面打开")
			return

		#self._util.zoom_in(self.d)
		#return

		#self._util.save_screen(self.d)
		#return

		#配置
		prt(self._config,title = "游戏配置信息")
		


		while True:
			#如果是果盘COC 点进入游戏
			self.GPstart()

			#打印统计
			#prt(self._count,title = "统计")
			ss(10,1, precent = 2)


	def Launch_app(self):
		self.d.app_start(self._app)

	def Stop_app(d):
		self.d.app_stop(self._app)

	def GPstart(self):
		EXISTS = lambda a,b: self.d(text=a, className=b).exists()
		CLICK = lambda a,b: self.d(text=a, className=b).click()
		#Watcher = lambda a,b:self.d.xpath("//*[@text="+ a +"]/../" + b).click()
		activity = self._util.current_act(self.d)
		
		if self._app == GameList[0] \
		and activity == 'com.flamingo.sdk.view.PluginActivity':
			try:
				if EXISTS("添加小号",TEXTVIEW):
					self._util.tap(self.d,416,131)
					ss(1)
				if EXISTS("登录",TEXTVIEW):
					CLICK("登录",TEXTVIEW)
					ss(1)
				if EXISTS("进入游戏",TEXTVIEW):
					CLICK("进入游戏",TEXTVIEW)
					if '果盘进入' in self._count:
						self._count['果盘进入'] += 1
						print("果盘游戏进入次数: ",self._count['果盘进入'], end="\r")
					else:
						self._count['果盘进入'] = 1 
					ss(1)
					self._util.tap(self.d,1,1,r = True)
				#Watcher("添加小号",TEXTVIEW)
			except Exception as e:
				ss(30,1)

		



		