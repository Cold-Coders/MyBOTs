#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import json,os,time,threading,logging
import tkinter.scrolledtext as ScrolledText
import tkinter.font


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
		#------------------Loading config------------------------------
		self.loading_config()	
		self.loading_languages()
		self.selecting_emulator()
		self.connect_device()
		#-------------------Basic Windows--------------------------------------

		
		self.window = tk.Tk()
		tk.Frame.__init__(self, self.window, *args, **kwargs)
		self.build_gui()
		self.test_area()
		self.information_show()


	def build_gui(self):                    
		# Build GUI
		self.window.title("My CoC Bots")
		self.window.resizable(width = False, height = False)
		self.window.geometry("800x800") #wxh
		self.window.option_add('*tearOff', 'FALSE')
		self.grid(column=0, row=0, sticky='ew')
		# self.grid_columnconfigure(0, weight=1, uniform='a')
		# self.grid_columnconfigure(1, weight=1, uniform='a')
		# self.grid_columnconfigure(2, weight=1, uniform='a')
		# self.grid_columnconfigure(3, weight=1, uniform='a')
		
		

		# Add text widget to display logging info
		st = ScrolledText.ScrolledText(self, state='disabled',width = 50, height = 25,bg = "black", fg = "white")
		st.configure(font='TkFixedFont')
		st.grid(column=0, row=0, sticky='w')

		# Create textLogger
		text_handler = TextHandler(st)

		# Logging configuration
		logging.basicConfig(filename='test.log',
			level=logging.INFO, 
			format='%(asctime)s - %(levelname)s - %(message)s')        

		# Add the handler to logger
		logger = logging.getLogger()        
		logger.addHandler(text_handler)
		self.set_buttons()
	
	def start(self):
		t1 = threading.Thread(target=worker, args=[])
		t1.daemon = True
		t1.start()
		self.window.mainloop()


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

	def set_buttons(self):
		CheckVar1 = IntVar()
		CheckVar2 = IntVar()
		CheckVar3 = IntVar()
		CheckVar4 = IntVar()
		CheckVar5 = IntVar()
		CheckVar6 = IntVar()
		donate = Checkbutton( text = "自动捐兵",variable = CheckVar1, onvalue = 1,
							 offvalue = 0, height = 1, width = 10)
		donate.place(x = 500, y = 30)
		auto_lose = Checkbutton( text = "自动掉杯",variable = CheckVar2, onvalue = 1,
							 offvalue = 0, height = 1, width = 10)
		auto_lose.place(x = 500, y = 60)
		auto_attack = Checkbutton( text = "自动打鱼",variable = CheckVar3, onvalue = 1,
							 offvalue = 0, height = 1, width = 10)
		auto_attack.place(x = 500, y = 90)
		extra_func1 = Checkbutton( text = "更多功能1",variable = CheckVar4, onvalue = 1,
							 offvalue = 0, height = 1, width = 10)
		extra_func1.place(x = 500, y = 120)
		extra_func2 = Checkbutton( text = "更多功能2",variable = CheckVar5, onvalue = 1,
							 offvalue = 0, height = 1, width = 10)
		extra_func2.place(x = 500, y = 150)
		extra_func3 = Checkbutton(text = "更多功能3",variable = CheckVar6, onvalue = 1,
							 offvalue = 0, height = 1, width = 10)
		extra_func3.place(x = 500, y = 180)
	
	def test_area(self):
		canva = Canvas(self.window,width=400,height=400,bg = "cyan")
		canva.place(x = 0,y = 400)
		canva.create_text(75,30,text = "测试区", fill="darkblue",font="Times 20 italic bold")
		button1 = Button(self.window, text = "缩放", anchor = W, highlightcolor = "red")
		button1.configure(width = 5, activebackground = "red", relief = FLAT)
		button1_window = canva.create_window(35, 60, anchor=NW, window=button1)
			   
		button2 = Button(self.window, text = "收集资源", anchor = W)
		button2.configure(width = 8, activebackground = "red", relief = FLAT)
		button2_window = canva.create_window(35, 100, anchor=NW, window=button2)

		button3 = Button(self.window, text = "捐兵测试", anchor = W)
		button3.configure(width = 8, activebackground = "red", relief = FLAT)
		button3_window = canva.create_window(35, 140, anchor=NW, window=button3)

		# one = tkinter.PhotoImage(file = r'lab.webp')
		# canva.create_image(200,200, image = one)

	def information_show(self):
		canva = Canvas(self.window,width=400,height=400,bg = "white")
		canva.place(x = 400,y = 400)
		canva.create_text(150,15,text = "游戏状态")
		canva.create_text(50,50,text = "金钱：",fill = "brown")
		canva.create_text(50,70,text = "红水：", fill = "red")
		canva.create_text(50,90,text = "黑水：")
		canva.create_text(73,140,text = "累计掠夺金币：", fill = "brown")
		canva.create_text(73,160,text = "累计掠夺红水：", fill = "red")
		canva.create_text(73,180,text = "累计掠夺黑水：")
