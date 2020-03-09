#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import json,os,time,threading,logging
import tkinter.scrolledtext as ScrolledText
import tkinter.font
from PIL import ImageTk
import PIL.Image


from subprocess import call
from tkinter import *
from tkinter import messagebox
from util import *


from COC.GUI.GUI_logs import *
from COC.GUI.GUI_util import *
from COC.GUI.GUI_emu  import *
from COC.GUI.GUI_util import GUI_Tools as G


from COC.Bot import COC_BOT

global Win
if not Win:
	import appscript

class COC_GUI(tk.Frame):
	# This class defines the graphical user interface 
	def __init__(self, *args, **kwargs):
		''' Variables
		self.config - type(dict) configure of Bot 				
			.config['lang'] - language of GUI
		self.lang   - type(dict) configure of language
		self.em 	- type(int) Emulator's pid
		self.d 		- type(str) Device's name before connect
					- type(obj) Device's automator engine after connected
		self.func   - type(List) Functionality of the bots 
		self.lang['func_name'] - type(List) name of Function #在语言配置里增加减少修改
					0 - 自动捐赠
					1 - 自动降杯
					2 - 自动打鱼

		self.lang['test_name'] - type(List) name of Function #在语言配置里
		self.test_button	   - type(List) button of test function
					0 - 缩放
					1 - 收集资源
					2 - 捐兵测试
		self.lang['info_name'] - type(List) name of Information board
					0 - "金钱"
					1 - "红水"
					2 - "黑水"
					3 - "累计掠夺金币"
					4 - "累计掠夺红水"
					5 - "累计掠夺黑水"
		'''

		#------------------Loading config------------------------------
		self.loading_config()	
		self.loading_languages()
		self.selecting_emulator()
		self.connect_device()  
		#-------------------Basic Windows--------------------------------------
		self.window = tk.Tk()
		tk.Frame.__init__(self, self.window, *args, **kwargs)
		self.window.title("My CoC Bots")
		self.window.resizable(width = False, height = False) 
		self.window.geometry("800x800") #wxh
		self.window.option_add('*tearOff', 'FALSE')
		self.grid(column=0, row=0, sticky='ew')

		self.loging_board()
		self.set_function()
		self.test_area()
		self.information_show()
	
	def start(self):
		t1 = threading.Thread(target=worker, args=[])
		t1.daemon = True
		t1.start()
		self.window.mainloop()


	def set_function(self):
		self.func = list()

		for i in range(len(self.lang['func_name'])):
			self.func.append(BooleanVar())
			donate = Checkbutton( text = self.lang['func_name'][i],variable = self.func[i],
			 					offvalue = 0, height = 1, width = 10)
			donate.place(x = 500, y = 430 + i*30)

	
	def test_area(self):
		canvas = Canvas(self.window,width=400,height=400,bg = "cyan")
		canvas.place(x = 0,y = 400)
		canvas.create_text(75,30,text = self.lang['Test_Area'], fill="darkblue",font="Times 20 italic bold")
		
		#------------------------background-----------------------------------------------
		self.img1 = tk.PhotoImage(file= "COC/res/elixir.png")
		bg = canvas.create_image(10,10,image=self.img1,anchor =NW)

		#------------------------test button saved in text_button-------------------------
		self.test_button = list()

		for i in range(len(self.lang['test_name'])):
			btn = Button(self.window, text = self.lang['test_name'][i],
						anchor = "center" , highlightcolor = "red")
			btn.configure(width = 14, activebackground = "red", relief = FLAT)
			canvas.create_window(35, 60 + i*40, anchor= NW , window=btn)
			self.test_button.append(btn)
		
		canvas.tag_lower(bg)

	def information_show(self):
		canva = Canvas(self.window,width=400,height=400,bg = "white")
		canva.place(x = 400,y = 0)
		#------------------------background-----------------------------------------------
		self.img2 = tk.PhotoImage(file= "COC/res/elixir.png")
		canva.create_image(20,20,image=self.img2,anchor =NW)

		#------------------------Information Board-------------------------
		canva.create_text(150,15,text = "游戏状态")
		fill_color = [
					  "brown",
					  "red",
					  "black"
					 ]
		for i in range(len(self.lang['info_name'])):
			canva.create_text(50,50 + 20*i,text = self.lang['info_name'][i],fill = fill_color[i%len(fill_color)])
		

	def loging_board(self):                    
		# Build GUI
		text = tk.Text(self.window, height = 1, width = 29 ,fg = "white", bg = "black", font="Times 20 italic bold")
		text.insert(INSERT,self.lang['log'])
		text.place(x = 0,y = 0)
		
		# Add text widget to display logging info
		st = ScrolledText.ScrolledText(self.window, state='disabled', width = 55, height = 35, bg = "black", fg = "white")
		st.configure(font='TkFixedFont')
		st.place(x = 0, y = 35)

		# Create textLogger
		text_handler = TextHandler(st)

		# Logging configuration
		logging.basicConfig(filename='test.log',
			level=logging.INFO, 
			format='%(asctime)s - %(levelname)s - %(message)s')        

		# Add the handler to logger
		logger = logging.getLogger()        
		logger.addHandler(text_handler)
		


	#uiautomator connect to a device
	def connect_device(self):
		#check the version of Uiautomator2
		try:
			call('pip install -U uiautomator2')
			call('pip3 install -U uiautomator2')
		except Exception as e:
			pass

	# selecting an emulator
	def selecting_emulator(self):
		self.em = None
		self.d = None

		devices = G.devices(r = True)

		if len(devices) < 1:
			messagebox.showinfo("Error", "Did not find the devices")
			exit()

		#choose from all devices
		Emulator(devices,self).start()
		
	# selecting a language
	def select_language(self):
		langs = {
				"中文":'chn',
				"English":'eng'
			}

		new_window = tk.Tk()
		btn = G.selection(new_window,"Languages",langs)
		
		def Set_lang(lang):
			new_window.destroy()
			self.config['lang'] = lang
			self.save_config()

		for b in btn:
			b['command']=lambda lang=b['text']:Set_lang(langs[lang])

		new_window.mainloop()		

	#loading config of languages
	def loading_languages(self):
		#if it is empty config or language is not set yet, 
		if 'lang' not in self.config.keys() or self.config['lang'] == '':
			self.select_language() #select a language
		
		#if there is a profile of language, loading the config
		try:
			self.lang = load_configure("COC/config/lang/" + self.config['lang'] + ".json")	
		except Exception as e: #exit if error
			#messagebox.showinfo("Error", "Did not find the language profile")
			self.config['lang'] = ''
			self.save_config()
			exit()

	#loading config by json file
	def loading_config(self):
		try:
			self.config = load_configure("COC/config/config.json")
		except Exception as e:
			self.config = {}
			self.save_config()


	#Saving the config into the file config.json
	def save_config(self):
		with open('COC/config/config.json', 'w',encoding='utf-8') as outfile:
				json.dump(self.config, outfile, ensure_ascii=False, indent=4, sort_keys=True)
