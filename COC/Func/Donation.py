import aircv as ac
import uiautomator2

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from GUI.GUI_logs import *
from GUI.GUI_utils import *
from COC.Func.Others import Utils as U

from util import *

class Donation:
	def __init__(self, GUI , resolution,coord):
		self.path = 'COC/recognition/' + resolution + "/Donation/"
		self.trainer_path  = 'COC/recognition/' + resolution + "/train/trainer/"
		self.train_path = 'COC/recognition/' + resolution + "/train/"

		self.d = GUI._config['d']

		self.lang = GUI.lang['Donation']
		self.count = GUI._count

		self.coordinator = coord["Donation"]
		self._Common = GUI._config["Common"]

		self.Area = self.coordinator['Area']
		self.buttons = self.coordinator['buttons']

		if 'Donation' not in GUI.config:
			self.init_config()
		else:
			self.config = GUI.config['Donation']

#----------------------- GUI ---------------------------------------
		self._select_troops = dict()
		self._select_spell = dict()
		self._select_siege = dict()

		self._amount_troops = dict()
		self._amount_spell = dict()
		self._amount_siege = dict()

		#self.close_donation = path + "close_donation.png"
		#self.trainer = trainer_path + "13.png"
		
		#self.req_btn = path + "request_" + GUI.config['lang'] + ".png"
		#self.req2_btn = path + "request2_" + GUI.config['lang'] + ".png"
		#self.donation_list = self.config["donation"]
		#self.train_list = list()
#----------------------- Utils ---------------------------------------
		def save_selected_value():
			for troop_name in self.config['donation']['troops'].keys():
				self.config['donation']['troops'][troop_name][2] = self._select_troops[troop_name].get()
				self.config['donation']['troops'][troop_name][3] = self._amount_troops[troop_name].get()
			for spell_name in self.config['donation']['spell'].keys():
				self.config['donation']['spell'][spell_name][2] = self._select_spell[spell_name].get()
				self.config['donation']['spell'][spell_name][3] = self._amount_spell[spell_name].get()
			for siege_name in self.config['donation']['siege'].keys():
				self.config['donation']['siege'][siege_name][2] = self._select_siege[siege_name].get()
				self.config['donation']['siege'][siege_name][3] = self._amount_siege[siege_name].get()
			GUI.config['Donation'] = self.config
			GUI.save_config()
			U.prt( "Donation config Saved",mode = 2)

		self.SAVE = lambda: save_selected_value()

#------------------------------Set up GUI-------------------------------#

	def set_donation(self,window):
		set_window = Toplevel(window)
		set_window.geometry("600x600")
		set_window.title(self.lang['titles']['window'])
		board = Canvas(set_window, width=600, height=600, bg = "white")
		board.place( x = 0, y = 0)
		







#------------------------------自定义模式-------------------------------#
		Label(board, text = self.lang['titles']['num'],bg = "white").place(x = 115, y = 425)
		Label(board, text = self.lang['titles']['num'],bg = "white").place(x = 315, y = 215)
		Label(board, text = self.lang['titles']['num'],bg = "white").place(x = 515, y = 5)
		
		for troop_name in self.config['donation']['troops'].keys():
			self._select_troops[troop_name] = BooleanVar(value = self.config['donation']['troops'][troop_name][2])
			donate = Checkbutton(board, text = self.lang['troops'][troop_name],
				variable = self._select_troops[troop_name],bg="white", height = 1, width = 10)
			donate.place(x = 400, y = 20 + self.config['donation']['troops'][troop_name][0]*30-20)
			self._amount_troops[troop_name] = IntVar(value = self.config['donation']['troops'][troop_name][3])
			amount = Entry(board, textvariable = self._amount_troops[troop_name],width = 5)
			amount.place(x = 515, y = 20 + self.config['donation']['troops'][troop_name][0]*30-20)

		for spell_name in self.config['donation']['spell'].keys():
			self._select_spell[spell_name] = BooleanVar(value = self.config['donation']['spell'][spell_name][2])
			donate = Checkbutton(board, text = self.lang['spell'][spell_name],
				variable = self._select_spell[spell_name],bg="white", height = 1, width = 10)
			donate.place(x = 200, y = 230 + self.config['donation']['spell'][spell_name][0]*30-20)
			self._amount_spell[spell_name] = IntVar(value = self.config['donation']['spell'][spell_name][3])
			amount = Entry(board, textvariable = self._amount_spell[spell_name],width = 5)
			amount.place(x = 315, y = 230 + self.config['donation']['spell'][spell_name][0]*30-20)

		for siege_name in self.config['donation']['siege'].keys():
			self._select_siege[siege_name] = BooleanVar(value = self.config['donation']['siege'][siege_name][2])
			donate = Checkbutton(board, text = self.lang['siege'][siege_name],
				variable = self._select_siege[siege_name],bg="white", height = 1, width = 10)
			donate.place(x = 0, y = 440 + self.config['donation']['siege'][siege_name][0]*30-20)
			self._amount_siege[siege_name] = IntVar(value = self.config['donation']['siege'][siege_name][3])
			amount = Entry(board, textvariable = self._amount_siege[siege_name],width = 5
				 )
			amount.place(x = 115, y = 440 + self.config['donation']['siege'][siege_name][0]*30-20)

		set_close(set_window, func = self.SAVE)


#------------------------------Initial configure-------------------------------#
	def init_config(self):
		self.config = {
				"donation": {
					"siege": {
						"barracks": [4,"undefined",0,1],
						"blimp": 	[2,"undefined",0,1],
						"slammer": 	[3,"undefined",0,1],
						"wall_wrecker": [1,"undefined",0,1]
					},
					"spell": {
						"bat": [11,"undefined",0,1],
						"clone": [6,"undefined",0,1],
						"earthquake": [8,"undefined",0,1],
						"freeze": [5,"undefined",0,1],
						"haste": [9,"undefined",0,1],
						"healing": [2,"undefined",0,1],
						"jump": [4,"undefined",0,1],
						"lightning": [1,"undefined",0,1],
						"poison": [7,"undefined",0,1],
						"rage": [3,"undefined",0,1],
						"skeleton": [10,"undefined",0,1]
					},
					"troops": {
						"baby_dragon": [7,"undefined",0,1],
						"balloon": [2,"undefined",0,1],
						"bowler": [17,"undefined",0,1],
						"dragon": [5,"undefined",0,1],
						"electro": [9,"undefined",0,1],
						"giant": [1,"undefined",0,1],
						"golem": [14,"undefined",0,1],
						"healer": [4,"undefined",0,1],
						"hog_rider": [12,"undefined",0,1],
						"ice_golem": [18,"undefined",0,1],
						"lava": [16,"undefined",0,1],
						"miner": [8,"undefined",0,1],
						"minion": [11,"undefined",0,1],
						"pekka": [6,"undefined",0,1],
						"valkyrie": [13,"undefined",0,1],
						"witch": [15,"undefined",0,1],
						"wizard": [3,"undefined",0,1],
						"yeti": [10,"undefined",0,1]
					}
				}
			}

	def donateOnce(self):
		pass
		#不在家乡界面则结束
		#打开兵营识别已有军队
		#不在聊天界面则打开聊天界面
		#找到多个捐赠按钮并记录
		#给每个捐赠按钮进行识别
		#点击捐赠
		#根据列表确定已经兵种
		#识别已有兵种并点击捐赠
		#关闭窗口
		'''#open the chat
								x,y = self.buttons['open_chat']
								U.tap(self.d,x,y)
								ss(3)
						
								# loop to find request
								x,y = U.find_PosbyArea(self.d, self.Area["chat_box"] , self.req_btn,confidence = 0.87)
								#while x != -1:
									# check what they want
									# offset( y - 30) x range ( 30 - 300) y range ( 60 )  x = 50 for one slot
								#crop = U.crop_screen(self.d.screenshot(format="opencv"),(30, y - 150, 300, y - 30 ) )
								if x != -1:
									pos = self.Area["donation_offset"]
									pos[1] += y
									pos[3] += y
									crop = U.crop_screen(self.d, pos)
						
									#if request exist U.find_PosbyArea(self.d, pos , self.req2_btn,confidence = 0.87)[0] != -1:
									if U.find_position(crop , self.req2_btn,confidence = 0.87)[0] != -1:
										
										#crop the first slot
										U.prt("找到捐赠请求图标,并点击")
										pos2 = self.Area["slot_offset"]
										pos2[1] += y
										pos2[3] += y
										crop2 = U.crop_screen(self.d, pos2)
										#U.save_screen(crop2,"donation")
										U.tap(self.d, x, y)
										ss(2)
						
										#x2,y2 = U.find_position(self.d , crop2 ,confidence = 0.9)
										x2,y2 = U.find_PosbyArea(self.d, self.Area["donation_box"] , crop2,confidence = 0.5)
										print(x2,y2)
										if x2 != -1:
											U.prt("在捐赠列表找到对应的兵,并点击(" + str(x2) + "," + str(y2) + ")捐赠")
											#click and to find if exist and click 3 times
											for i in range(r_num(lbound = 3)):
												U.tap(self.d,x2,y2)
											ss(1)
										else:
											U.prt("未找到对应兵种,加入训练列表", mode = 2)
											self.train_list.append(crop)
											U.save_screen(crop2,"donation")
						
										#os.remove("donation.png")
						
									else:
										U.prt("未设置捐赠种类")
						
						
								else:
									U.prt("未找到捐赠按钮" , mode = 2)
								#close the chat
								x,y = self.buttons['close_chat']
								U.tap(self.d,x,y)'''
#--------------------------------------------------------------------------------#								
'''	chat_x,chat_y = self.buttons['open_chat']
		U.tap(self.d,chat_x,chat_y)  #打开聊天室
		ss(3)


		donate_x,donate_y = U.find_PosbyArea(self.d, self.Area["chat_box"] , self.req_btn,confidence = 0.87)
		if donate_x != -1:
			U.tap(self.d,donate_x,donate_y) #点击捐赠按钮
			tag = 1 #继续捐赠

			for type in self.donation_list:
				for kind in self.donation_list[type]:
					if self.donation_list[type][kind][2] == 1: #判断是否所勾选种类 是的话继续操作
						while True:
							kind_x,kind_y = U.find_PosbyArea(self.d, self.Area["donation_box"] , self.donation_list[type][kind][1],confidence = 0.87)  #根据图片位置去找在捐赠区域是否有可捐赠的兵种
							if kind_x != -1:
								U.tap(self.d,kind_x,kind_y) #点击捐兵

							else:
								break
		close_x,close_y = U.find_PosbyArea(self.d, self.Area["donation_box"] , self.close_donation,confidence = 0.87)
		U.tap(self.d,close_x,close_y)
		close_chat_x, close_chat_y = self.buttons['close_chat']
		U.tap(self.d,close_chat_x,close_chat_y)

'''
 #一开始是满的情况下 捐一次造一次

'''
def train(self):
	t_x,t_y =  U.find_PosbyArea(self.d, self.Area["whole_screen"] , self.trainer,confidence = 0.87)
	U.tap(self.d,t_x,t_y)
	for type in self.donation_list:
				for kind in self.donation_list[type]:
					if self.donation_list[type][kind][2] == 1: #判断是否所勾选种类 是的话继续操作
						while True:
							kind_x,kind_y = U.find_PosbyArea(self.d, self.Area["donation_box"] , train_path + kind + ".png",confidence = 0.87)  #根据图片位置去找在捐赠区域是否有可训练的兵种
							if kind_x != -1:
								U.tap(self.d,kind_x,kind_y) #点击造兵

							else:
								break
	close_train_x,close_train_y = self.buttons["close_train"]
	U.tap(self.d,close_train_x,close_train_y)


'''