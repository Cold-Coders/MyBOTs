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

		self.d = GUI._config['d']

		self.lang = GUI.lang['Donation']
		self.count = GUI._count

		self.coordinator = coord["Donation"]
		self._Common = GUI._config["Common"]

		self.Area = self.coordinator['Area']
		self.buttons = self.coordinator['buttons']
		
		self.init_config(GUI.config)

#----------------------- GUI ---------------------------------------
		self._select_troops = dict()
		self._select_spell = dict()
		self._select_siege = dict()

		self._limitation = [IntVar() for i in range(3)]
		self._amount_troops = dict()
		self._selections = [StringVar() for i in range(5)]
		#self.close_donation = path + "close_donation.png"
		#self.trainer = trainer_path + "13.png"

#----------------------- Special Img ---------------------------------------
		self.req_btn = self.path + "request_" + GUI.config['lang'] + ".png"
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
			for i in range(len(self.config['train_limits'])):
				self.config['train_limits'][i] = self._limitation[i].get()

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
		
		def change_limit(eventObject):
			if self._selections[0].get() == self.lang["schema"][0]:
				self._limitation[0].set(500000)
				self._limitation[1].set(100000)
				self._limitation[2].set(0)
			elif self._selections[0].get() == self.lang["schema"][1]:
				self._limitation[0].set(50000)
				self._limitation[1].set(10000)
				self._limitation[2].set(0)
				print("自动修改最低限制测试")

		place_selection(self,board,100,5,values = self.lang["schema"], array = self._selections[0], width = 30,\
			callback = change_limit)
		place_selection(self,board,100,35,values = list(self.lang['troops'].values()), array = self._selections[1],\
			callback = change_limit)
		place_selection(self,board,100,65,values = list(self.lang['troops'].values()), array = self._selections[2],\
			callback = change_limit)
		place_selection(self,board,100,95,values = list(self.lang['spell'].values()), array = self._selections[3],\
			callback = change_limit)
		place_selection(self,board,100,125,values = list(self.lang['siege'].values()), array = self._selections[4],\
			callback = change_limit)

		for i in range(len(self.config['selections'])):
			self._selections[i].set(self.config['selections'][i])

		count = 0
		for amount in self.config['amounts'].keys():
				self._amount_troops[amount] = IntVar(value = self.config['amounts'][amount])
				Label(board, text = self.lang['titles']['num'] + ":",bg = "white",\
					font='黑体 13 bold',width = 10).place(x = 195, y = 35 + count * 30)
				Entry(board, textvariable = self._amount_troops[amount],width = 5).place(x = 280, y = 35 + count * 30)
				count += 1
#------------------------------通用设置-------------------------------#
		Label(board, text = self.lang['titles']['gold_limit'],bg = "white",\
			font='黑体 13' ).place(x = 10, y = 155)
		Label(board, text = self.lang['titles']['elixir_limit'],bg = "white",\
			font='黑体 13' ).place(x = 10, y = 185)
		Label(board, text = self.lang['titles']['dart_limit'],bg = "white",\
			font='黑体 13' ).place(x = 10, y = 215)
		
		for i in range(3):
			Entry(board, textvariable = self._limitation[i],width = 15).place(x = 100, y =  155 + i*30)
			Label(board, text = self.lang['titles']['no_train'],bg = "white",\
			font='黑体 13' ).place(x = 220, y =  155 + i*30)

		for i in range(len(self.config['train_limits'])):
				self._limitation[i].set(self.config['train_limits'][i])
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
	def init_config(self, config):
		init = {
				"amounts":{
						"troop1" : 0,
						"troop2" : 0,
						"spell"  : 0,
						"siege"	 : 0
				},
				"train_limits":[500000,100000,0],
				"selections": [self.lang["schema"][0],"","","",""],
				"donation": {
					"siege": {
						"barracks": [4,"undefined",False],
						"blimp": 	[2,"undefined",False],
						"slammer": 	[3,"undefined",False],
						"wall_wrecker": [1,"siege/wall_wrecker.png",False]
					},
					"spell": {
						"bat": [11,"undefined",False],
						"clone": [6,"undefined",False],
						"earthquake": [8,"undefined",False],
						"freeze": [5,"spell/freeze.png",False],
						"haste": [9,"undefined",False],
						"healing": [2,"undefined",False],
						"jump": [4,"undefined",False],
						"lightning": [1,"undefined",False],
						"poison": [7,"undefined",False],
						"rage": [3,"spell/rage.png",False],
						"skeleton": [10,"undefined",False]
					},
					"troops": {
						"baby_dragon": [7,"undefined",False],
						"balloon": [2,"troops/balloon.png",False],
						"bowler": [17,"undefined",False],
						"dragon": [5,"undefined",False],
						"electro": [9,"troops/electro.png",False],
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

		if 'Donation' not in config:
			self.config = init
			return

		for key in init:
			if key not in config['Donation']:
				self.config = init
				return

		self.config = config['Donation']


#------------------------------ train -------------------------------#
	def tap(self, pos, times = 1):
			if pos == None:
				print("没有提供坐标")
				return
			elif len(pos) == 2:
				x,y = pos
			elif len(pos) == 3:
				x,y,z = pos

			for i in range(times):
				U.tap(self.d,x,y)
			ss()

	def produce_troops(self):

		# 1. 确定地图在townhall
		screen = self.d.screenshot(format="opencv")
		if not self._Common.Scense(screen,spec = 1):
			print("不在家乡界面")
			return
		# 2. 根据配置 确定资源
		if self.count['gold'] < self.config['train_limits'][0]\
			or self.count['elixir'] < self.config['train_limits'][1]\
			or self.count['dart_elixir'] < self.config['train_limits'][2]:
			print("训练资源不够")
			return
		# 3. 打开兵营界面
		self.tap(self.buttons['train'])
		# 4. 根据配置点相应位置
			# 专用雷龙配置 9雷龙 2气球 4狂暴 3冰冻 3战车
		if self.config['selections'][0] == self.lang["schema"][0]:
			#依次训练部队,法术,工程机器
			self.tap(self.buttons['troops']['btn'])
			self.tap(self.buttons['troops']['electro'],times = 9)
			self.tap(self.buttons['troops']['balloon'],times = 2)

			self.tap(self.buttons['spells']['btn'])
			self.tap(self.buttons['spells']['freeze'],times = 3)
			self.tap(self.buttons['spells']['rage'],times = 4)

			self.tap(self.buttons['sieges']['btn'])
			self.tap(self.buttons['sieges']['wall_wrecker'],times = 3)
		#self.lang['troops'].values()
		#self.lang['spell'].values()
		#self.lang['siege'].values()

		# 5. 关闭训练界面
		self.tap(self.buttons['close_train'])

#------------------------------ Donate -------------------------------#
	def donateOnce(self):

		self.count["donation"] += 1

		# 1. 打开兵营造兵
		self.produce_troops()
		# 2. 确定地图
		where = self._Common.Scense(self.d.screenshot(format="opencv"))
		# townhall 点聊天
		if where == 1:
			self.tap(self.buttons['open_chat'])
			where = self._Common.Scense(self.d.screenshot(format="opencv"))

		# 在聊天界面 
		if where == 6:
			# 3. 找捐兵按钮
			x,y = U.find_PosbyArea(self.d, self.Area["chat_box"] , self.req_btn,confidence = 0.87)

			# 1. 处理捐赠信息
			result = self.process_request(x,y)
			if not type(result) is dict:
				self.tap(self.buttons['close_chat'])
				msg = result + self.lang['msgs']['counts'] + str(self.count['donation'])
				U.msg(self.d, msg, mode = 2,times = 3)
				return False

			# 2. 进行捐赠操作
			return self.process_donation(result)

		#聊天窗则关掉捐兵窗口
		where = self._Common.Scense(self.d.screenshot(format="opencv"))
		if where == 6:
			self.tap(self.buttons['close_chat'])
		return False
#------------------------------ Donation Process -------------------------------#
	def process_request(self,x,y): #return False for error
		#没有找到捐兵按钮
		if x == -1:
			return self.lang['msgs']['no_find']
		
		info = dict()
		info['x'] = x
		info['y'] = y
		#截取特定区域 给定兵种 直接返回
		#无给定兵种 截取文字分析
		return info

	def process_donation(self,info):

		def get_key(my_dict,val): 
			for key, value in my_dict.items(): 
				 if val == value: 
					 return key 
			return None

		pos = (info['x'],info['y'])
		self.tap(pos)

		ss(2)
		screen = self.d.screenshot(format="opencv")
		# 捐兵模式1 特定兵种,找到就点完事.
		troops = self.config["donation"]["troops"]
		spells = self.config["donation"]["spell"]
		siege = self.config["donation"]["siege"]

		if self.config['selections'][0] == self.lang["schema"][0]:
			# 找到对应图就点击
			self.find_tap(self.path + troops["balloon"][1])
			self.find_tap(self.path + troops["electro"][1])
			
			self.find_tap(self.path + spells["freeze"][1],times = 2)
			self.find_tap(self.path + spells["rage"][1])

			self.find_tap(self.path + siege["wall_wrecker"][1])

			#应该检测关掉捐兵窗口
			#U.tap(self.d,100,300,r = True)
			ss()
			self._Common.Scense(screen, spec = 9)
			ss(2)
			self._Common.Scense(self.d.screenshot(format="opencv"), spec = 11)
			
			return True

		return False
#------------------------------- Utils -------------------------------#
	def find_tap(self,img,times = 1,confidence = 0.8):
		if img == self.path + "undefined":
		 	print("未定义查找图片")
		 	return

		print(img)
		pos = U.find_position(self.d , img ,confidence = confidence)
		self.tap(pos,times = times)
		ss()

'''
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




'''
#open the chat
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
								U.tap(self.d,x,y)

#--------------------------------------------------------------------------------#								
	chat_x,chat_y = self.buttons['open_chat']
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
		Donation_once(self):
	tap("open_chatbox")
	x,y = find_pos("捐赠按钮")
	上滑次数 = 0
	while x = -1:
		if 上滑次数 > 5：
			exit
		上滑（）
		上滑次数 + = 1
		x,y = find_pos("捐赠按钮")
	tap(x,y)
	for troop in 配置文件['troops']
		if troop.checkvalue = 1:
			x,y = find_pos(troop,donate_area)
			while x != -1:
				tap(x,y)
				x,y = find_pos(troop,donate_area)
	for spell in 配置文件['spells']
		if spell.checkvalue = 1:
			x,y = find_pos(spell,donate_area)
			while x != -1:
				tap(x,y)
				x,y = find_pos(spell,donate_area)
	for siege in 配置文件['sieges']
		if siege.checkvalue = 1:
			x,y = find_pos(siege,donate_area)
			while x != -1:
				tap(x,y)
				x,y = find_pos(siege,donate_area)
	c_x,c_y = find_pos(close_button,donate_area)
	tap(c_x,c_y)
	tap('close_chat')
		
	

#----------------------------捐兵伪代码-------------------------------

Donation_once(self):                       
	tap("open_chatbox")
	x,y = find_pos("捐赠按钮")
	上滑次数 = 0
	while x = -1:
		if 上滑次数 > 5：
			exit
		上滑（）
		上滑次数 + = 1
		x,y = find_pos("捐赠按钮")
	tap(x,y)
	for i in range(troop1_amount):             #之前用while的时候可以无限捐 比如有人要9个气球 我们这边设定3个的话就只能捐3个 但是用while的的话可以一直捐 但是那样会破坏造兵平衡
		x,y = find_pos(troop2,donate_area)		#不论实际上捐的数量，就按配置默认的数量来进行点击，不论需不需要，多点击了没事
					for i in (0,troop1_amount):
		if x != -1
			tap(x,y)	

	for j in range(troop2_amount):
		x,y = find_pos(troop2,donate_area)
		if x != -1
			tap(x,y)

	for j in range(spell_amount):
		x,y = find_pos(spell,donate_area)
		if x != -1
			tap(x,y)		
		

	for z in range(0.siege_amount)
		x,y = find_pos(siege,donate_area)
			if x != -1:
				tap(x,y)
				
	c_x,c_y = find_pos(close_button,donate_area)
	tap(c_x,c_y)
	tap('close_chat')
'''