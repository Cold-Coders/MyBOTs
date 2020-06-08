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
import re

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

		self._count = { 
				"gold" : -1 ,
				"elixir" : -1,
				"dart_elixir" : -1,
				"c_gold" : 0,
				"c_elixir": 0,
				"c_dart_elixir": 0,
				"labor": 0,
				"builder": 0,
				"zoom_out": 0
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
				self.config['obstacle'][obs_name][1] = self._select_obstacle[obs_name].get()
			GUI.config['General'] = self.config
			GUI.save_config()
			U.prt( "General config Saved",mode = 2)

		self.SAVE = lambda: save_selected_value()



#----收集资源-------------------------------------------------------------------------------------
	def collect_resourse(self):

		def tap(img,msg):
			x,y = U.find_position(screen, self.path + img, confidence = 0.90)
			if x != -1:
				U.tap(self.d,x,y)
				U.prt(msg,mode = 1)
			#else:
				#U.prt(self.lang['msgs'][4],mode = 3)

		screen = self.d.screenshot(format="opencv")

		if self._count['zoom_out'] < 10:
			U.zoom_out(self.d)
			self._count['zoom_out'] += 1

		before = [  self._count['gold'],
					self._count['elixir'],
					self._count['dart_elixir']
				]
				
		where = self._Common.Scense(screen)
		if where == 1:
			tap(self.config['elixir'],self.lang['msgs'][0]) #0.99205
			tap(self.config['gold'], self.lang['msgs'][1])
			tap(self.config['dart_elixir'],self.lang['msgs'][2])
			self.update_cum_resourse(before)

		elif where == 2:
			tap(self.config['b_elixir'],self.lang['msgs'][0])
			tap(self.config['b_gold'],self.lang['msgs'][1])
			tap(self.config['gem'],self.lang['msgs'][3])
		
		else:
			print("搜集资源 - 不在家乡或者建筑地图 Code",where)


#----统计增加资源---------------------------------------------------------------------------------
	def update_cum_resourse(self, before):
		if self._count['gold'] == -1 or self._count['elixir'] == -1 or self._count['dart_elixir'] == -1:
			return
		
		self.Update_info()
		
		ss(1)

		dif_gold = (self._count['gold'] - before[0])
		dif_elixir = (self._count['elixir'] - before[1])
		dif_d_elixir = (self._count['dart_elixir'] - before[2])

		if dif_gold > 0:
			self._count['c_gold'] +=  d_gold 
			self._infoboard[3]['text'] = self._count['c_gold']

		if dif_elixir > 0:
			self._count['c_elixir'] += dif_elixir
			self._infoboard[4]['text'] = self._count['c_elixir']

		if dif_d_elixir > 0:
			self._count['c_dart_elixir'] += dif_d_elixir
			self._infoboard[5]['text'] = self._count['c_dart_elixir']
		
#----更新资源状态-------------------------------------------------------------------------------------
	def ORC(self, screen,area, Accurate = False, Debug = False, lang = "num"):
			text = ""
			#baidu
			if self.orc == 1:
				text = U.BdOrc(screen, area , Accurate = Accurate)
			elif self.orc == 2:
				text = U.orcbyArea(screen, area,lang = lang, Debug = Debug)
			
			#new_text = ""
			#for word in text:
			#	if word in "1234567890":
			#		new_text += word
			#	elif word in "/":
			#		break
			return re.sub('[^A-Za-z0-9/]+', '', text)

	def Update_info(self):
		#gem_color = (208, 236, 120)
		#
		screen = self.d.screenshot(format="opencv")
		
		where = self._Common.Scense(screen)
		if where != 1 and where != 2:
			print("识别资源 - 不在家乡或者建筑地图 Code",where)
			return
		#--------------Gold---------------------------------
		gold = self.ORC(screen, self.Area["gold"])
		if gold.isdigit():
			gold = int(gold)
			self._infoboard[0]['text'] = gold
		else:
			self._infoboard[0]['text'] = self.lang['recog_error']

		#--------------Elixir---------------------------------
		elixir = self.ORC(screen, self.Area["elixir"])
		if elixir.isdigit():
			elixir = int(elixir)
			self._infoboard[1]['text'] = elixir
		else:
			self._infoboard[0]['text'] = self.lang['recog_error']

		#--------------dart Elixir---------------------------------
		dart_elixir = self.ORC(screen, self.Area["d_elixir"])
		if dart_elixir.isdigit():
			dart_elixir = int(dart_elixir)
			self._infoboard[2]['text'] = dart_elixir
		else:
			self._infoboard[0]['text'] = self.lang['recog_error']

		if where == 1:
			self.Image_to_homebase()
			self._count['gold'] = gold
			self._count['elixir'] = elixir
			self._count['dart_elixir'] = dart_elixir
		else:
			self.Image_to_builder()


#-------------------Remove obstacle-------------------------------#
	def remove_single_obstacle(self):
		
		#判定资源大于1万
		if self._count['elixir'] < 10000 or self._count['gold'] < 10000:
			U.prt(self.lang['msgs'][5] ,mode = 1)
			return

		#判定地图 与 判定是否有工人
		screen = self.d.screenshot(format="opencv")
		if self._Common.Scense(screen,spec = 1):
			self.labors(screen)
			if self._count['labor'] < 1:
				U.prt(self.lang['msgs'][7] ,mode = 1)
				return

		elif self._Common.Scense(screen,spec = 2):
			self.labors(screen, home = False)
			if self._count["builder"] < 1:
				U.prt(self.lang['msgs'][7] ,mode = 1)
				return

		else:
			U.prt(self.lang['msgs'][6] ,mode = 1)

			return

		#灌木
		#35 180 190
		#43 220 255
		#4

		tag = True
		rx,ry = self.buttons["remove_obstacle"]

		for obs in self._select_obstacle.keys():
			move_val = self._select_obstacle[obs].get()
			if move_val == True:
				x,y = U.find_position(screen, self.path + self.config['obstacle'][obs][1],confidence = 0.75)
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

		labor = self.ORC(screen, self.Area["labor"]) if home else self.ORC(screen, self.Area["builder"])
		
		if home:
			self._count['labor'] = int(labor[0]) if labor[0].isdigit() else -1
			self._infoboard[6]['text'] = labor
		else:
			self._count['builder'] = int(labor[0]) if labor[0].isdigit() else -1
			self._infoboard[7]['text'] = labor

			#self._infoboard[6]['text'] = self.lang['recog_error']
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

		count = 1
		for obs_name in self.config['obstacle'].keys():
			self._select_obstacle[obs_name] = tkinter.BooleanVar(value = self.config['obstacle'][obs_name][1])
			donate = Checkbutton(board, text = self.lang['obstacle_name'][obs_name],
				variable = self._select_obstacle[obs_name],bg="white", height = 1, width = 10)
			donate.place(x = 10, y = 20 + count*30-20)
			place_image(self,board,self.path + self.config['obstacle'][obs_name][0],110,\
				25 + count*30-20,resize = (20,20))
			#place_label(self,board,130,y = 20 + self.config['obstacle'][obs_name][0]*30-20,text=self.config['obstacle'][obs_name][1])
			count += 1
		#点关闭后保存配置 set_close(root, func = 函数)
		set_close(set_window, func = self.SAVE)
		#Test SAVE configure
		#self._select_obstacle["gem_box"].set(False)
		#self.SAVE()
		
	def init_config(self):
		self.config = {
					"GUI_path" : "COC/res/obstacle",
					"obstacle" : {
									"gem_box" :  ["Gem_10x9.png",True,0.8],
									"mushroom": ["Mushroom_9x9.png",True,0.8],
									"stone_s" : ["Stone_9x7.png",True,0.8],
									"stone_m" : ["Stone_11x9.png",True,0.8],
									"stone_l" : ["Stone_14x15.png",True,0.8],
									"tree_s"  : ["Tree_12x9.png",True,0.8],
									"tree_m"  : ["Tree1_16x14.png",True,0.8],
									"tree_l"  : ["Tree2_16x18.png",True,0.8],
									"trunk_ver": ["Trunk_7x14.png",True,0.8],
									"trunk_hor": ["Trunk_11x9.png",True,0.8]
								  },
					"elixir" : "elixir_19x19.png",
					"gold"	 : "gold_18x18.png",
					"dart_elixir" : "dart_elixir_19x19.png",
					"b_elixir": "b_elixir_18x18.png",
					"b_gold": "b_gold_16x16.png",
					"gem" : "b_gem_18x17.png"
			}