import aircv as ac
import uiautomator2

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from GUI.GUI_logs import *
from COC.Func.Others import Utils as U

from util import *

class Donation:
	def __init__(self, GUI , resolution):
		self.d = GUI._config['d']
		self.lang = GUI.lang
		
		path = 'COC/recognition/' + resolution + "/Donation/"
		self.req_btn = path + "request_" + GUI.config['lang'] + ".png"
		self.req2_btn = path + "request2_" + GUI.config['lang'] + ".png"
		Area = {
					"860x732":{
								"chat_box":   (0,0,310,732),
								"donation_offset": [30,-145,300,-30],
								"slot_offset": [45,-80,75,-50],
								"donation_box": (310,0,860,732)
							  }
		}
		self.Area = Area[resolution]

		buttons = {
					"860x732":{
								"open_chat": (20,380),
								"close_chat":(331,384)
							  }
		}
		self.buttons = buttons[resolution]


		if 'Donation' not in GUI.config:
			self.config = {

			}
		else:
			self.config = GUI.config['Donation']

		self.train_list = list()

	def donateOnce(self):
		#open the chat
		x,y = self.buttons['open_chat']
		U.tap(self.d,x,y)
		ss(2)

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
				x2,y2 = U.find_PosbyArea(self.d, self.Area["donation_box"] , crop2)
				#print()
				if x2 != -1:
					U.prt("在捐赠列表找到对应的兵,并点击(" + str(x2) + "," + str(y2) + ")捐赠")
					#click and to find if exist and click 3 times
					for i in range(r_num(lbound = 3)):
						U.tap(self.d,x2,y2)
					ss(1)
				else:
					U.prt("未找到对应兵种，加入训练列表"， mode = 2)
					self.train_list.append(crop)

				#os.remove("donation.png")

			else:
				U.prt("未设置捐赠种类")

		else:
			U.prt("未找到捐赠按钮" ， mode = 2)
		#close the chat
		x,y = self.buttons['close_chat']
		U.tap(self.d,x,y)



