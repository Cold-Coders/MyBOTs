import aircv as ac
import uiautomator2
from util import *

from GUI.GUI_logs import *
from COC.Func.Others import Utils as U

class General:
	def __init__(self, d , orc):
		self.d = d
		self.orc = orc
		h,w = self.d.window_size()
		self.resolution = str(w) + "x" + str(h)
		path = 'COC/recognition/' + self.resolution + "/Resource/"

		self.elixir = [ path + "elixir_8x8.png"]
		self.gold   = [ path + "gold_8x8.png",
						path + "gold_18x18.png"]

		self.Area = {
		"860x732":{
					"gold": (700,20,800,40)
				  
				  }
		}


	def collect_resourse(self,d):

		tag = True

		for img in self.elixir:
			x,y = U.find_position(d,img,confidence = 0.85)
			if x != -1:
				U.tap(d,x,y)
				U.prt("click elixir at point (" + str(x) + "," + str(y) + ")" ,mode = 1)
				tag = False
				break
		if tag:
			U.prt("Didn't find elixir" ,mode = 3)

		tag = True
		for img in self.gold:
			x,y = U.find_position(d,img,confidence = 0.87)
			if x != -1:
				U.tap(d,x,y)
				U.prt("click gold at point (" + str(x) + "," + str(y) + ")" ,mode = 1)
				tag = False
				break
		if tag:
			U.prt("Didn't find gold" ,mode = 3)

	def Update_info(self,d):
		def orc(screen,area, Accurate = False):
			#baidu
			if self.orc == 1:
				U.BdOrc(screen, area , Accurate = Accurate)
			elif self.orc == 2:
				U.orcbyArea(screen, area )
		screen = d.screenshot(format="opencv")

		gold_Area = self.Area[self.resolution]["gold"]
		gold = orc(screen, gold_Area)
		#U.prt( "Gold " + gold,mode = 2)
		return 1
