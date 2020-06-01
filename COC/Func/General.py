import aircv as ac
import uiautomator2

import tkinter
from tkinter import *
from tkinter import messagebox

from GUI.GUI_logs import *
from COC.Func.Others import Utils as U

from GUI.GUI_utils import *
from util import *

from PIL import ImageTk
import PIL.Image

class General:
	def __init__(self, GUI , resolution):
		self.d = GUI._config['d']
		self.orc = GUI.config['orc']
		self.lang = GUI.lang['General']

		self._select_obstacle = dict()
		self._select_troops = dict()
		self._select_spell = dict()
		self._select_siege = dict()

		self.path = 'COC/recognition/' + resolution + "/Resource/"

		self.elixir = [ self.path + "elixir_8x8.png"]

		self.gold = [ self.path + "gold_8x8.png",
					  self.path + "gold_18x18.png"]

		self.obstacle = [   self.path + "Gem_10x9.png",
							self.path + "Mushroom_9x9.png",
							self.path + "Stone_9x7.png",
							self.path + "Stone_11x9.png",
							self.path + "Stone_14x15.png",
							self.path + "Tree_12x9.png",
							self.path + "Tree1_16x14.png",
							self.path + "Tree2_16x18.png",
							self.path + "Trunk_7x14.png",
							self.path + "Trunk_11x9.png"
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
					"GUI_path" : "COC/res/obstacle",
					"obstacle" : {
									"gem_box" :  [1,"Gem_10x9.png",True],
									"mushroom": [2,"Mushroom_9x9.png",True],
									"stone_s" : [3,"Stone_9x7.png",True],
									"stone_m" : [4,"Stone_11x9.png",True],
									"stone_l" : [5,"Stone_14x15.png",True],
									"tree_s"  : [6,"Tree_12x9.png",True],
									"tree_m"  : [7,"Tree1_16x14.png",True],
									"tree_l"  : [8,"Tree2_16x18.png",True],
									"trunk_ver": [9,"Trunk_7x14.png",True],
									"trunk_hor": [10,"Trunk_11x9.png",True]
								  }
			}
		else:
			self.config =  GUI.config['General']
			prt(self.config,title = "General 配置信息")

		self.change_to_gem = lambda: GUI.right_part.itemconfig(
				GUI.list_info_widget[2],image = GUI.builder_img[2])

		def change_to_builderbase(imgs):
			for i in range(len(imgs)):
				GUI.right_part.itemconfig(
					GUI.list_info_widget[i],image = imgs[i])

		self.Image_to_builder = lambda: change_to_builderbase(GUI.builder_img)
		self.Image_to_homebase = lambda: change_to_builderbase(GUI.homevillage_img)
		
		def save_selected_value():
			for obs_name in self._select_obstacle.keys():
				self.config['obstacle'][obs_name][2] = self._select_obstacle[obs_name].get()
			GUI.save_config()
			U.prt( "config Saved",mode = 2)

		self.SAVE = lambda: save_selected_value()

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

	def place_image(self,frame,image,x,y):
		img =PIL.Image.open(image)
		self.img = ImageTk.PhotoImage(img)
		frame.create_image(x,y,image=self.img,anchor = NW)

#-------------------Remove obstacle-------------------------------#
	def set_obstacle(self,window):
		set_window = Toplevel(window)
		set_window.geometry("200x420")	
		w = Canvas(set_window, width=200, height=110)
		self.place_image(w,"COC/res/obstacle.png",0,0)
		w.place( x = 0, y = 310)

		for obs_name in self.config['obstacle'].keys():
			self._select_obstacle[obs_name] = tkinter.BooleanVar(value = self.config['obstacle'][obs_name][2])
			donate = Checkbutton(set_window, text = self.lang['obstacle_name'][obs_name],
				variable = self._select_obstacle[obs_name],bg="white", height = 1, width = 10)
			donate.place(x = 10, y = 0 + self.config['obstacle'][obs_name][0]*30-20)

		#点关闭后保存配置 set_close(root, func = 函数)
		set_close(set_window, func = self.SAVE)
		#Test SAVE configure
		#self._select_obstacle["gem_box"].set(False)
		#self.SAVE()

	def remove_single_obstacle(self):
		tag = True
		rx,ry = self.buttons["remove_obstacle"]

		for obs in self.config['obstacle']:
			move_val = self._select_obstacle[obs].get()
			if move_val == True:
				x,y = U.find_position(self.d, self.path + self.config['obstacle'][obs][1],confidence = 0.7)
				if x != -1:
					U.tap(self.d,x,y)
					U.prt("remove obstacle at (" + str(x) + "," + str(y) + ")" ,mode = 1)
					#if it enough resourse to remove
					U.tap(self.d,rx,ry)
					tag = False
					break

		if tag:
			U.prt("Didn't find any removable obstacle",mode = 3)

#------------------------------Donation-------------------------------#

	def set_donation(self,window):
		set_window = Toplevel(window)
		set_window.geometry("500x600")
		w = Canvas(set_window, width=120, height=132)
		self.place_image(w,"COC/res/electron_dragon.png",0,0)
		w.place( x = 300, y = 300)	
		for troop_name in self.config['donation']['troops'].keys():
			self._select_troops[troop_name] = tkinter.BooleanVar(value = self.config['donation']['troops'][troop_name][2])
			donate = Checkbutton(set_window, text = self.lang['donation']['troops'][troop_name],
				variable = self._select_troops[troop_name],bg="white", height = 1, width = 10)
			donate.place(x = 10, y = 0 + self.config['donation']['troops'][troop_name][0]*30-20)

		for spell_name in self.config['donation']['spell'].keys():
			self._select_spell[spell_name] = tkinter.BooleanVar(value = self.config['donation']['spell'][spell_name][2])
			donate = Checkbutton(set_window, text = self.lang['donation']['spell'][spell_name],
				variable = self._select_spell[spell_name],bg="white", height = 1, width = 10)
			donate.place(x = 110, y = 0 + self.config['donation']['spell'][spell_name][0]*30-20)

		for siege_name in self.config['donation']['siege'].keys():
			self._select_siege[siege_name] = tkinter.BooleanVar(value = self.config['donation']['siege'][siege_name][2])
			donate = Checkbutton(set_window, text = self.lang['donation']['siege'][siege_name],
				variable = self._select_siege[siege_name],bg="white", height = 1, width = 10)
			donate.place(x = 210, y = 0 + self.config['donation']['siege'][siege_name][0]*30-20)

		set_close(set_window, func = self.SAVE)

	def donate(self):
		tag = True