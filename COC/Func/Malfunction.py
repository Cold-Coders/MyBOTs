import aircv as ac
import uiautomator2
from util import *

from GUI.GUI_logs import *
from COC.Func.Others import Utils as U

class Upgrade:

	def __init__(self, d):
		self.d = d

		h,w = self.d.window_size()
		self.resolution = str(w) + "x" + str(h)

		path = 'COC/recognition/' + self.resolution + "/Others/"

		self.redcross = path + "redcross.png"

		self.Area = {
					"860x732":{
								"worker": (700,20,800,40)
							  }
		}

		self.buttons = {
					"860x732":{
								"worker" :  (330,30)
							  }
		}

	def close_window(self):
		pass	
