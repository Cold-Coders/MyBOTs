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

		self.obstacle = [ path + "Gem_10x9.png",
						  path + "Mushroom_9x9.png",
						  path + "Stone_9x7.png",
						  path + "Stone_11x9.png",
						  path + "Stone_14x15.png",
						  path + "Tree_12x9.png",
						  path + "Tree1_16x14.png",
						  path + "Tree2_16x18.png",
						  path + "Trunk_7x14.png",
						  path + "Trunk_11x9.png"
						]

		self.Area = {
					"860x732":{
								"gold": (700,20,800,40),
								"elixir": (700,70,800,90)
							  }
		}

		self.buttons = {
					"860x732":{
								"remove_obstacle": (427,630)
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
			text = ""
			#baidu
			if self.orc == 1:
				text = U.BdOrc(screen, area , Accurate = Accurate)
			elif self.orc == 2:
				text = U.orcbyArea(screen, area )
			
			new_text = ""
			for word in text:
				if word in "1234567890":
					new_text += word
			return new_text

		screen = d.screenshot(format="opencv")

		gold_Area = self.Area[self.resolution]["gold"]
		gold = orc(screen, gold_Area)
		

		elixir_Area = self.Area[self.resolution]["elixir"]
		elixir = orc(screen, elixir_Area)

		U.prt( "Gold " + gold + " Elixir " + elixir,mode = 2)
		if gold.isdigit() and elixir.isdigit():
			return ( int(gold) , int(elixir) )
		else:
			return (-1,-1)

	def remove_single_obstacle(self,d):
		tag = True
		rx,ry = self.buttons[self.resolution]["remove_obstacle"]

		for img in self.obstacle:
			x,y = U.find_position(d,img,confidence = 0.85)
			if x != -1:
				U.tap(d,x,y)
				U.prt("remove obstacle at (" + str(x) + "," + str(y) + ")" ,mode = 1)
				
				U.tap(d,rx,ry)
				tag = False
				break
		if tag:
			U.prt("Didn't find any obstacle" ,mode = 3)