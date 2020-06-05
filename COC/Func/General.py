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


		self._count = { 
				"gold" : 0 ,
				"elixir" : 0,
				"dart_elixir" : 0,
				"c_gold" : 0,
				"c_elixir": 0,
				"c_dart_elixir": 0,
				"labor": 0
		}

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
			U.prt( "General config Saved",mode = 2)

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
	def ORC(self, screen,area, Accurate = False, Debug = False, lang = "num"):
			text = ""
			#baidu
			if self.orc == 1:
				text = U.BdOrc(screen, area , Accurate = Accurate)
			elif self.orc == 2:
				text = U.orcbyArea(screen, area,lang = lang, Debug = Debug)
			
			new_text = ""
			for word in text:
				if word in "1234567890":
					new_text += word
				elif word in "/":
					break
			return new_text

	def Update_info(self):
		#gem_color = (208, 236, 120)
		
		screen = self.d.screenshot(format="opencv")
		if self._Common.Scense(screen,spec = 1, Debug = True):
			self.Image_to_homebase()
			cumulative = True
		elif self._Common.Scense(screen,spec = 2):
			self.Image_to_builder()
			cumulative = False
		else:
			print("识别资源 - 不在家乡或者建筑地图")
			return
		#--------------Gold---------------------------------
		gold_Area = self.Area["gold"]
		gold = self.ORC(screen, gold_Area)
		if gold.isdigit():
			gold = int(gold)
			if cumulative:
				self._count['c_gold'] += (gold - self._count['gold']) \
					if self._count['gold'] != 0 and (gold - self._count['gold']) > 0 else 0
				self._count['gold'] = gold
			self._infoboard[0]['text'] = gold
			self._infoboard[3]['text'] = self._count['c_gold']


		else:
			self._infoboard[0]['text'] = self.lang['recog_error']

		#--------------Elixir---------------------------------
		elixir_Area = self.Area["elixir"]
		elixir = self.ORC(screen, elixir_Area)
		if elixir.isdigit():
			elixir = int(elixir)
			if cumulative:
				self._count['c_elixir'] += (elixir - self._count['elixir']) \
					if self._count['elixir'] != 0 and (elixir - self._count['elixir']) > 0 else 0
				self._count['elixir'] = elixir
			self._infoboard[1]['text'] = elixir
			self._infoboard[4]['text'] = self._count['c_elixir']
		else:
			self._infoboard[0]['text'] = self.lang['recog_error']

		#--------------dart Elixir---------------------------------
		dart_elixir_Area = self.Area["d_elixir"]
		dart_elixir = self.ORC(screen, dart_elixir_Area)
		if dart_elixir.isdigit():
			dart_elixir = int(dart_elixir)
			if cumulative:
				self._count['c_dart_elixir'] += (dart_elixir - self._count['dart_elixir']) \
					if self._count['dart_elixir'] != 0 and (dart_elixir - self._count['dart_elixir']) > 0 else 0
				self._count['dart_elixir'] = dart_elixir
			self._infoboard[2]['text'] = dart_elixir
			self._infoboard[5]['text'] = self._count['c_dart_elixir']

		else:
			self._infoboard[0]['text'] = self.lang['recog_error']

#-------------------Remove obstacle-------------------------------#
	def remove_single_obstacle(self):
		
		
		#判定地图
		screen = self.d.screenshot(format="opencv")
		if self._Common.Scense(screen,spec = 1):
			self.labors(screen)
		elif self._Common.Scense(screen,spec = 2):
			self.labors(screen, home = False)
		else:
			U.prt(self.lang['msgs'][6] ,mode = 1)
			return

		#判定是否有工人
		if self._count['labor'] < 1:
			U.prt(self.lang['msgs'][7] ,mode = 1)
			return


		#判定资源大于1万
		if self._count['elixir'] < 10000 or self._count['gold'] < 10000:
			U.prt(self.lang['msgs'][5] ,mode = 1)
			return

		tag = True
		rx,ry = self.buttons["remove_obstacle"]

		for obs in self.config['obstacle']:
			move_val = self._select_obstacle[obs].get()
			if move_val == True:
				x,y = U.find_position(screen, self.path + self.config['obstacle'][obs][1],confidence = 0.7)
				if x != -1:
					U.tap(self.d,x,y)
					U.prt(self.lang['obstacle_name'][obs] + " (" + str(x) + "," + str(y) + ")" ,mode = 1)
					#if it enough resourse to remove
					U.tap(self.d,rx,ry)
					tag = False
					break

		if tag:
			U.prt("Didn't find any removable obstacle",mode = 3)

	def labors(self, screen, home = True):
		if home:
			labor_Area = self.Area["labor"]
			labor = self.ORC(screen, labor_Area,Debug = True)
			if labor.isdigit():
				self._count['labor'] = int(labor)
				self._infoboard[6]['text'] = self._count['labor']
			else:
				self._infoboard[6]['text'] = self.lang['recog_error']
		else:
			pass

#-------------------General Setting GUI-------------------------------#
	def set_general(self,window):
		set_window = Toplevel(window)
		set_window.geometry("420x420")	
		set_window.title(self.lang['title'])

		board = Canvas(set_window, width=420, height=420,bg = "white")
		board.place( x = 0, y = 0)

		#place_image(self,board,"COC/res/dragon.png",0,0)
		place_label(self,board,10,5,text="勾选移除障碍物:           等待时间设置:",\
			font='Helvetica 13 bold')

		for obs_name in self.config['obstacle'].keys():
			self._select_obstacle[obs_name] = tkinter.BooleanVar(value = self.config['obstacle'][obs_name][2])
			donate = Checkbutton(board, text = self.lang['obstacle_name'][obs_name],
				variable = self._select_obstacle[obs_name],bg="white", height = 1, width = 10)
			donate.place(x = 10, y = 20 + self.config['obstacle'][obs_name][0]*30-20)
			place_image(self,board,self.path + self.config['obstacle'][obs_name][1],110,\
				25 + self.config['obstacle'][obs_name][0]*30-20,resize = (20,20))
			#place_label(self,board,130,y = 20 + self.config['obstacle'][obs_name][0]*30-20,text=self.config['obstacle'][obs_name][1])

		#点关闭后保存配置 set_close(root, func = 函数)
		set_close(set_window, func = self.SAVE)
		#Test SAVE configure
		#self._select_obstacle["gem_box"].set(False)
		#self.SAVE()
		
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
					"b_gold": "b_gold_17x17.png",
					"gem" : "b_gem_18x17.png"
			}