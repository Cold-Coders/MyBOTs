import threading
from util import *
from CONSTANT import *
from COC.Func.Others import Utils as u
from GUI.GUI_logs import *


#模拟器分辨需求为 860x732 dpi 160
class COC_BOT():

	def __init__(self,config,lang):

		self._error = 0
		self._config = config
		self._lang = lang
		self.d = self._config['d']

		prt(self._config,title = "配置信息")
		u.prt("机器信息",self.d.info)

		self.Check_profil()

		self._app = config['game']
		self._count = dict()

	def run(self):
		#配置
		while True:
			#如果是果盘COC 点进入游戏
			self.GPstart()

			#打印统计
			#prt(self._count,title = "统计")
			ss(10,1, precent = 2)

	def Check_profil(self):
		#If it is not emulator, skip
		if 'emu' not in self._config:
			return

		height,width = self.d.window_size()
		if height != 732 and width != 860:
			u.prt(self._lang["resolution_error"])


	def Launch_app(self):
		self.d.app_start(self._app)

	def Stop_app(d):
		self.d.app_stop(self._app)

	def GPstart(self):
		EXISTS = lambda a,b: self.d(text=a, className=b).exists()
		CLICK = lambda a,b: self.d(text=a, className=b).click()
		#Watcher = lambda a,b:self.d.xpath("//*[@text="+ a +"]/../" + b).click()
		activity = u.current_act(self.d)
		
		if self._app == 'com.supercell.clashofclans.guopan' \
		and activity == 'com.flamingo.sdk.view.PluginActivity':
			try:
				if EXISTS("添加小号",TEXTVIEW):
					u.tap(self.d,416,131)
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
					u.tap(self.d,1,1,r = True)
				#Watcher("添加小号",TEXTVIEW)
			except Exception as e:
				ss(30,1)

		



		