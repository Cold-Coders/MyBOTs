import aircv as ac
import uiautomator2
from util import *

from GUI.GUI_logs import *
from COC.Func.Others import Utils as U

class Upgrade:

	def __init__(self, GUI, resolution):
		self.d = GUI._config['d']
		
		path = 'COC/recognition/' + resolution + "/Upgrade/"

		suggests = {
					"eng" : path + "suggest_eng.png",
					"chn" : path + "suggest_chn.png"
		}

		Area = {
					"worker": (700,20,800,40),
					"wokring": (111,111,111,11),
		}

		buttons = {
					"worker" :  (330,30),
					"upgrade1": (427,630),
					"upgrade2":	(438,530)
		}

	def check_Worker(self):
		pass	

	def Suggest_upgrade(self):
		pass

	def is_enough(self):
		pass
		#always has the last zero
		#simple to check if the zero is red or white

	def upgradde_hero(self):
		pass

