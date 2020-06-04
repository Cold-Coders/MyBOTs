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
	def __init__(self, GUI , resolution, coord):
		self.d = GUI._config['d']
		self.orc = GUI.config['orc']
		self.lang = GUI.lang['General']
		self.path = 'COC/recognition/' + resolution + "/Resource/"

		self.coordinator = coord["General"]
		self._Common = GUI._config["Common"]

		self._select_obstacle = dict()
		self.Area = self.coordinator['Area']
		self.buttons = self.coordinator['buttons']

		#self.info_text[i]['text']
		self._infoboard = GUI.info_text


		#第一次收集资源时的缩放
		self.first = True
		self.b_first = True

		if 'General' not in GUI.config:
			self.init_config()
		else:
			self.config =  GUI.config['General']
			prt(self.config,title = "General 配置信息")

#----------------------------------------------------------------------------------------------------
		self.change_to_gem = lambda: GUI.right_part.itemconfig(
				GUI.list_info_widget[2],image = GUI.builder_img[2])

		def change_to_builderbase(imgs,title):
			for i in range(len(imgs)):
				GUI.right_part.itemconfig(
					GUI.list_info_widget[i],image = imgs[i])
			GUI.info_title.set(GUI.lang["titles"]["HomeVillage"] if title == 1 else GUI.lang["titles"]["BuilderBase"])

		self.Image_to_builder = lambda: change_to_builderbase(GUI.builder_img,2)
		self.Image_to_homebase = lambda: change_to_builderbase(GUI.homevillage_img,1)
		
		def save_selected_value():
			for obs_name in self._select_obstacle.keys():
				self.config['obstacle'][obs_name][2] = self._select_obstacle[obs_name].get()
			GUI.save_config()
			U.prt( "config Saved",mode = 2)

		self.SAVE = lambda: save_selected_value()


#----收集资源-------------------------------------------------------------------------------------
	def collect_resourse(self):

		def tap(xy,msg):
			if xy[0] != -1:
				U.tap(self.d,xy[0],xy[1])
				U.prt(msg,mode = 1)
			#else:
				#U.prt(self.lang['msgs'][4],mode = 3)

		screen = self.d.screenshot(format="opencv")

		try:
			if self._Common.Scense(screen,spec = 1):

				if self.first:
					U.zoom_out(self.d)
					self.first = False

				tap(U.find_position(screen, self.path + self.config['elixir'],\
				 confidence = 0.85),self.lang['msgs'][0])
				tap(U.find_position(screen, self.path + self.config['gold'],\
				 confidence = 0.85),self.lang['msgs'][1])
				tap(U.find_position(screen, self.path + self.config['dart_elixir'],\
				 confidence = 0.85),self.lang['msgs'][2])

			elif self._Common.Scense(screen,spec = 2):

				if self.b_first:
					U.zoom_out(self.d)
					self.b_first = False

				tap(U.find_position(screen, self.path + self.config['b_elixir'],\
				 confidence = 0.85),self.lang['msgs'][0])
				tap(U.find_position(screen, self.path + self.config['b_gold'],\
				 confidence = 0.85),self.lang['msgs'][1])
				tap(U.find_position(screen, self.path + self.config['gem'],\
				 confidence = 0.85),self.lang['msgs'][3])
			else:
				return

		except Exception as e:
			self.init_config()
		

#----更新资源状态-------------------------------------------------------------------------------------
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

		#gem_color = (208, 236, 120)
		screen = self.d.screenshot(format="opencv")
		if self._Common.Scense(screen,spec = 1):
			self.Image_to_homebase()
		elif self._Common.Scense(screen,spec = 2):
			self.Image_to_builder()
		else:
			return
		#--------------Gold---------------------------------
		gold_Area = self.Area["gold"]
		gold = orc(screen, gold_Area)
		if gold.isdigit():
			self._infoboard[0]['text'] = gold
		else:
			self._infoboard[0]['text'] = self.lang['recog_error']

		#--------------Elixir---------------------------------
		elixir_Area = self.Area["elixir"]
		elixir = orc(screen, elixir_Area)
		if elixir.isdigit():
			self._infoboard[1]['text'] = elixir
		else:
			self._infoboard[0]['text'] = self.lang['recog_error']

		#--------------dart Elixir---------------------------------
		dart_elixir_Area = self.Area["d_elixir"]
		dart_elixir = orc(screen, dart_elixir_Area)
		if dart_elixir.isdigit():
			self._infoboard[2]['text'] = dart_elixir
		else:
			self._infoboard[0]['text'] = self.lang['recog_error']


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


	def init_config(self):
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
								  },
					"elixir" : "elixir_19x19.png",
					"gold"	 : "gold_18x18.png",
					"dart_elixir" : "dart_elixir_19x19.png",
					"b_elixir": "b_elixir_18x18.png",
					"b_gold": "b_gold_19x18.png",
					"gem" : "b_gem_18x17.png"
			}