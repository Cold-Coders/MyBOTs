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
		self._selections = [StringVar() for i in range(5)]
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
			for spell_name in self.config['donation']['spell'].keys():
				self.config['donation']['spell'][spell_name][2] = self._select_spell[spell_name].get()
			for siege_name in self.config['donation']['siege'].keys():
				self.config['donation']['siege'][siege_name][2] = self._select_siege[siege_name].get()
			for amount in self.config['amounts'].keys():
				self.config['amounts'][amount] = self._amount_troops[amount].get()
			
			for i in range(len(self.config['selections'])):
				self.config['selections'][i] = self._selections[i].get()

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
		

		Label(board, text = self.lang['titles']['schema'],bg = "white",\
			font='黑体 13 bold',width = 10 ).place(x = 5, y = 5)
		Label(board, text = self.lang['titles']['troops'] + "1:",bg = "white",\
			font='黑体 13 bold',width = 10).place(x = 5, y = 35)
		Label(board, text = self.lang['titles']['troops'] + "2:",bg = "white",\
			font='黑体 13 bold',width = 10).place(x = 5, y = 65)
		Label(board, text = self.lang['titles']['spell']  + ":",bg = "white",\
			font='黑体 13 bold',width = 10).place(x = 5, y = 95)
		Label(board, text = self.lang['titles']['siege']  + ":",bg = "white",\
			font='黑体 13 bold',width = 10).place(x = 5, y = 125)
		
		place_selection(self,board,100,5,values = self.lang["schema"], array = self._selections[0],width = 30)
		place_selection(self,board,100,35,values = list(self.lang['troops'].values()), array = self._selections[1])
		place_selection(self,board,100,65,values = list(self.lang['troops'].values()), array = self._selections[2])
		place_selection(self,board,100,95,values = list(self.lang['spell'].values()), array = self._selections[3])
		place_selection(self,board,100,125,values = list(self.lang['siege'].values()), array = self._selections[4])

		for i in range(len(self.config['selections'])):
			self._selections[i].set(self.config['selections'][i])

		count = 0
		for amount in self.config['amounts'].keys():
				self._amount_troops[amount] = IntVar(value = self.config['amounts'][amount])
				Label(board, text = self.lang['titles']['num'] + ":",bg = "white",\
					font='黑体 13 bold',width = 10).place(x = 195, y = 35 + count * 30)
				Entry(board, textvariable = self._amount_troops[amount],width = 5).place(x = 280, y = 35 + count * 30)
				count += 1
		
		#	amount = Entry(board, textvariable = self._amount_troops[troop_name],width = 5)
		#	amount.place(x = 515, y = 20 + self.config['donation']['troops'][troop_name][0]*30-20)
#------------------------------自定义模式-------------------------------#
		Label(board, text = self.lang['titles']['siege'],bg = "white").place(x = 300, y = 425)
		Label(board, text = self.lang['titles']['spell'],bg = "white").place(x = 420, y = 215)
		Label(board, text = self.lang['titles']['troops'],bg = "white").place(x = 520, y = 5)
		for troop_name in self.config['donation']['troops'].keys():
			self._select_troops[troop_name] = BooleanVar(value = self.config['donation']['troops'][troop_name][2])
			donate = Checkbutton(board, text = self.lang['troops'][troop_name],
				variable = self._select_troops[troop_name],bg="white", height = 1, width = 10)
			donate.place(x = 480, y = 20 + self.config['donation']['troops'][troop_name][0]*30-20)
			
		for spell_name in self.config['donation']['spell'].keys():
			self._select_spell[spell_name] = BooleanVar(value = self.config['donation']['spell'][spell_name][2])
			donate = Checkbutton(board, text = self.lang['spell'][spell_name],
				variable = self._select_spell[spell_name],bg="white", height = 1, width = 10)
			donate.place(x = 380, y = 230 + self.config['donation']['spell'][spell_name][0]*30-20)

		for siege_name in self.config['donation']['siege'].keys():
			self._select_siege[siege_name] = BooleanVar(value = self.config['donation']['siege'][siege_name][2])
			donate = Checkbutton(board, text = self.lang['siege'][siege_name],
				variable = self._select_siege[siege_name],bg="white", height = 1, width = 10)
			donate.place(x = 280, y = 440 + self.config['donation']['siege'][siege_name][0]*30-20)
		set_close(set_window, func = self.SAVE)


#------------------------------Initial configure-------------------------------#
	def init_config(self):
		self.config = {
				"amounts":{
						"troop1" : 0,
						"troop2" : 0,
						"spell"  : 0,
						"siege"	 : 0
				},
				"selections": ["","","","",""],
				"donation": {
					"siege": {
						"barracks": [4,"undefined",False],
						"blimp": 	[2,"undefined",False],
						"slammer": 	[3,"undefined",False],
						"wall_wrecker": [1,"undefined",False]
					},
					"spell": {
						"bat": [11,"undefined",False],
						"clone": [6,"undefined",False],
						"earthquake": [8,"undefined",False],
						"freeze": [5,"undefined",False],
						"haste": [9,"undefined",False],
						"healing": [2,"undefined",False],
						"jump": [4,"undefined",False],
						"lightning": [1,"undefined",False],
						"poison": [7,"undefined",False],
						"rage": [3,"undefined",False],
						"skeleton": [10,"undefined",False]
					},
					"troops": {
						"baby_dragon": [7,"undefined",False],
						"balloon": [2,"undefined",False],
						"bowler": [17,"undefined",False],
						"dragon": [5,"undefined",False],
						"electro": [9,"undefined",False],
						"giant": [1,"undefined",False],
						"golem": [14,"undefined",False],
						"healer": [4,"undefined",False],
						"hog_rider": [12,"undefined",False],
						"ice_golem": [18,"undefined",False],
						"lava": [16,"undefined",False],
						"miner": [8,"undefined",False],
						"minion": [11,"undefined",False],
						"pekka": [6,"undefined",False],
						"valkyrie": [13,"undefined",False],
						"witch": [15,"undefined",False],
						"wizard": [3,"undefined",False],
						"yeti": [10,"undefined",False]
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