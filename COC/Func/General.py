import aircv as ac
import uiautomator2

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from GUI.GUI_logs import *
from COC.Func.Others import Utils as U

from util import *

class General:
	def __init__(self, GUI , resolution):
		self.d = GUI._config['d']
		self.orc = GUI.config['orc']
		self.lang = GUI.lang['General']

		path = 'COC/recognition/' + resolution + "/Resource/"

		self.elixir = [ path + "elixir_8x8.png"]

		self.gold = [ path + "gold_8x8.png",
					  path + "gold_18x18.png"]

		self.obstacle = [   path + "Gem_10x9.png",
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


		Area = {
					"860x732":{
								"gold":   (700,20,805,40),
								"elixir": (700,70,805,90),
								"d_elixir" :  (710,120,805,140)
							  }
		}
		self.Area = Area[resolution]


		buttons = {
					"860x732":{
								"remove_obstacle": (427,630),
								"gem_color" : (820,131),
								"remove_red" :(433,605)
							  }
		}
		self.buttons = buttons[resolution]


		if 'General' not in GUI.config:
			self.config = {

			}
		else:
			self.config =  GUI.config['General']

		self.change_to_gem = lambda: GUI.right_part.itemconfig(
				GUI.list_info_widget[2],image = GUI.builder_img[2])

		def change_to_builderbase(imgs):
			for i in range(len(imgs)):
				GUI.right_part.itemconfig(
					GUI.list_info_widget[i],image = imgs[i])

		self.Image_to_builder = lambda: change_to_builderbase(GUI.builder_img)
		self.Image_to_homebase = lambda: change_to_builderbase(GUI.homevillage_img)

	def collect_resourse(self):

		tag = True

		for img in self.elixir:
			x,y = U.find_position(self.d,img,confidence = 0.85)
			if x != -1:
				U.tap(self.d,x,y)
				U.prt("click elixir at point (" + str(x) + "," + str(y) + ")" ,mode = 1)
				tag = False
				break
		if tag:
			U.prt("Didn't find elixir" ,mode = 3)

		tag = True
		for img in self.gold:
			x,y = U.find_position(self.d,img,confidence = 0.87)
			if x != -1:
				U.tap(self.d,x,y)
				U.prt("click gold at point (" + str(x) + "," + str(y) + ")" ,mode = 1)
				tag = False
				break
		if tag:
			U.prt("Didn't find gold" ,mode = 3)

	def Update_info(self):
		
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

		screen = self.d.screenshot(format="opencv")

		gold_Area = self.Area["gold"]
		gold = orc(screen, gold_Area)
		

		elixir_Area = self.Area["elixir"]
		elixir = orc(screen, elixir_Area)

		dart_elixir_Area = self.Area["d_elixir"]
		dart_elixir = orc(screen, dart_elixir_Area)
		
		#check 9 pixel around (208, 236, 120)
		gem_x,gem_y = self.buttons['gem_color']
		gem_color = (208, 236, 120)
		flag = False
		for i in range(3):
			for j in range(3):
				pos = (gem_x + i,gem_y + j)
				if not U.isColor(screen,pos,gem_color,diff = 10):
					flag = True
					break
		if flag:
			self.Image_to_homebase()
		else:
			self.Image_to_builder()

		U.prt( "Gold " + gold + " Elixir " + elixir + " Dart_elixir/Gem " + dart_elixir,mode = 2)
		if gold.isdigit() and elixir.isdigit():
			if dart_elixir.isdigit():
				return ( int(gold) , int(elixir), int(dart_elixir) )
			return ( int(gold) , int(elixir), 0 )
		else:
			return (-1,-1,-1)


	def set_obstacle(self,window):
		set_window = Toplevel(window)
		set_window.geometry("100x250")
		button = Button(set_window, text="Do nothing button")
		button.pack()


	def remove_single_obstacle(self):
		tag = True
		rx,ry = self.buttons["remove_obstacle"]

		for img in self.obstacle:
			x,y = U.find_position(self.d,img,confidence = 0.7)
			if x != -1:
				U.tap(self.d,x,y)
				U.prt("remove obstacle at (" + str(x) + "," + str(y) + ")" ,mode = 1)
				#if it enough resourse to remove
				U.tap(self.d,rx,ry)
				tag = False
				break

		if tag:
			U.prt("Didn't find any removable obstacle",mode = 3)