#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import json,os,time,threading,logging

from PIL import ImageTk
import PIL.Image

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from util import *

from GUI.GUI_logs import *

from COC.COC_Bot import COC_BOT
from COC.Func.Others import Utils as U
from COC.Func.General import General
from COC.Func.Upgrade import Upgrade
from COC.Func.Emu_restarter import Emu_restarter as restarter


if not sys.platform == 'win32':
	import appscript


class COC_BOT_GUI(tk.Frame):
	# This class defines the graphical user interface 
	def __init__(self,config, *args, **kwargs):
		#------------------Loading config------------------------------
		self.config = {}
		self._config = config
		self.loading_config()	
		self.loading_languages()
		#-------------------Basic Windows--------------------------------------
		self.window = tk.Tk()
		tk.Frame.__init__(self, self.window, *args, **kwargs)

		self.check_resolution()
		self.init_Func()

		self.build_basic_window()
		self.build_left_part()
		self.build_right_part()
		self.build_menu()

	def start(self):
		def update():
			MyBot = COC_BOT(self._config,self.lang,self)
			MyBot.run()
			#while True:
			#	time.sleep(1)

		info_update = threading.Thread(target=update, args=[])
		info_update.daemon = True
		info_update.start()

		self.window.mainloop()

	def init_Func(self):
		h,w = self.d.window_size()
		resolution = str(w) + "x" + str(h)
		self._config["General"] = General(self.d,self.config['orc'],resolution)
		self._config["Upgrade"] = Upgrade(self.d,self.config['lang'],resolution)

	def check_resolution(self):
		#If it is not emulator, skip
		if 'emu' not in self._config:
			return

		height,width = self.d.window_size()
		if height != 732 and width != 860:
			U.prt(self.lang["tips"]["resolution_error"],mode = 3)
			reopen = messagebox.askyesno(self.lang["titles"]["error"], self.lang["tips"]["resolution_error"])
			if reopen:
				restarter.Emu(self._config,self.lang)
			else:
				u.prt(self.lang["tips"]["close_bot"],mode = 3)
				ss(5)
				self.window.destroy()
				exit()


	def build_menu(self):
		def donothing():
		   filewin = Toplevel(self.window)
		   button = Button(filewin, text="Do nothing button")
		   button.pack()

		menubar = Menu(self.window)

		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="New", command=donothing)

		filemenu.add_separator()

		filemenu.add_command(label="Exit", command=self.window.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label="Undo", command=donothing)

		editmenu.add_separator()

		editmenu.add_command(label="Cut", command=donothing)
		editmenu.add_command(label="Copy", command=donothing)
		editmenu.add_command(label="Paste", command=donothing)
		editmenu.add_command(label="Delete", command=donothing)
		editmenu.add_command(label="Select All", command=donothing)

		menubar.add_cascade(label="Edit", menu=editmenu)
		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="Help Index", command=donothing)
		helpmenu.add_command(label="About...", command=donothing)
		menubar.add_cascade(label="Help", menu=helpmenu)

		self.window.config(menu=menubar)


	def build_right_part(self):
		self.right_part = Canvas(self.window,bg = "white",width=400,height=800)
		self.right_part.grid(row = 0, column = 1 ,rowspan = 2, sticky=N+S+E+W)
		self.set_information()
		self.set_function()
		self.test_area()

		self.place_image(self.right_part,"COC/res/dragon.png",150,300)


	def place_image(self,frame,image,x,y):
		img =PIL.Image.open(image)
		self.img = ImageTk.PhotoImage(img)
		frame.create_image(x,y,image=self.img,anchor = NW)


	def test_area(self):
		self.right_part.create_text(75,530,text = self.lang['Test_Area'], fill="darkblue",font="Times 20 italic bold")
		#------------------------background-----------------------------------------------
		#self.logo = tk.PhotoImage(file = "COC/res/COC_logo.png")
		self.logo = PIL.Image.open(self.config['coc_logo'])
		#image = image.resize((20, 20))
		self.logo = ImageTk.PhotoImage(self.logo)
		self.right_part.create_image(230,720,image=self.logo,anchor = NW)
		
		#------------------------test button saved in text_button-------------------------
		self.test_button = list()

		for i in range(len(self.lang['test_name'])):
			btn = Button(self.right_part, text = self.lang['test_name'][i],
						anchor = "center" , highlightcolor = "red")
			btn.configure(width = 14, activebackground = "red", relief = FLAT)
			self.right_part.create_window(30 + (i%3*120) , 560 + (i//3) *40, anchor= NW , window=btn)
			self.test_button.append(btn)

		# find imgs
		def search_imgs():
			if not sys.platform == 'win32':
				find_img = "ls | grep '.png'"
			else:
				find_img = "dir | findstr '.png'"

			stream = os.popen(find_img)
			self.img_list = stream.read().split()

			self.testfind = ttk.Combobox(self.right_part,values=self.img_list)
			self.right_part.create_window(30 , 560 + 4 *40 + 10, anchor= NW , window=self.testfind)

		#Zoom out
		self.test_button[0]['command']= lambda: U.zoom_out(self.d)
		#Screen shot
		def new_shot():
			U.save_screen(self.d)
			search_imgs()


		self.test_button[1]['command']= lambda: new_shot()
		#Recognize information
		def updateinfo():
			info = self._config["General"].Update_info(self.d)
			for i in range(len(info)):
				self.info_text[i]['text'] = info[i]

		self.test_button[2]['command']= lambda: updateinfo()
		#Collect resourse
		self.test_button[3]['command']= lambda: self._config["General"].collect_resourse(self.d)
		#Remove obstacle once
		self.test_button[4]['command']= lambda: self._config["General"].remove_single_obstacle(self.d)

		#Find test
		search_imgs()
		#self.testfind = ttk.Combobox(self.right_part,values=self.img_list)
		#self.right_part.create_window(30 , 560 + 4 *40 + 10, anchor= NW , window=self.testfind)

		self.find = Button(self.right_part, text = self.lang['titles']['find'],
						anchor = "center" , highlightcolor = "red",
						command = lambda: U.test_read_img(self.d, self.testfind.get()))
		self.right_part.create_window(30 , 560 + 5 *40, anchor= NW , window=self.find)

		# 刷新查找列表
		self.refresh = Button(self.right_part, text = self.lang['titles']['refresh'],
						anchor = "center" , highlightcolor = "red",
						command = lambda: search_imgs())
		self.right_part.create_window(75 , 560 + 5 *40, anchor= NW , window=self.refresh)

		#将识别的图片进行处理,文件名与截图前面一直 末尾为_g
		self.pre_orc = Button(self.right_part, text = self.lang['titles']['revert_test'],
						anchor = "center" , highlightcolor = "red",
						command = lambda: U.revert_test() )
		self.right_part.create_window(140 , 560 + 5 *40, anchor= NW , window=self.pre_orc)




	def set_function(self):
		self.func = list()
		for i in range(len(self.lang['func_name'])):
			self.func.append(BooleanVar())
			donate = Checkbutton(self.right_part, text = self.lang['func_name'][i],
				variable = self.func[i],bg="white", offvalue = 0, height = 1, width = 10)
			donate.place(x = 20, y = 330 + i*30)

	def set_information(self):
		#------------------------background-----------------------------------------------
		# self.img2 = tk.PhotoImage(file= "COC/res/elixir.png")
		# canva.create_image(20,20,image=self.img2,anchor =NW)
		#------------------------Information Board-------------------------
		self.right_part.create_text(75,15,text = "游戏状态", fill="darkblue",font="Times 20 italic bold")
		fill_color = [
					  "brown",
					  "red",
					  "black"
					 ]
		self.list_pic = list()
		self.info_text = list()
		for i in range(len(self.lang['info_name'])):
			self.right_part.create_text(110,50 + 40*i,text = self.lang['info_name'][i],fill = fill_color[i%len(fill_color)])
			
			label = tk.Label(self.right_part, text = "0", relief="flat", background = "white")
			label.place(x = 200, y = 40 + 40*i)
			self.info_text.append(label)

			image = PIL.Image.open(self.config['source_image'][i])
			#image = image.resize((20, 20))
			image = ImageTk.PhotoImage(image)
			self.list_pic.append(image)
			self.right_part.create_image(20,30 + 40 * i, image = self.list_pic[i], anchor = NW)
		

	def build_left_part(self):                    
		# Build Left Part log
		text = tk.Text(self.frame, height = 0.15, fg = "white", bg = "black", font="Times 20 italic bold")
		text.insert(INSERT,self.lang['log'])
		text.grid(row = 0,column = 0, sticky=N+E+W)

		MyLogUi(self.frame,height = 59).grid(row = 1, column = 0)


	def build_basic_window(self):
		#------------------------set up windows and title-------------------------
		self.window.title("My CoC Bots")
		self.window.geometry("800x800") #wxh
		self.window.maxsize(1000, 800)
		self.window.minsize(800, 800)
		#self.window.resizable(width = False, height = False)
		self.window.option_add('*tearOff', 'FALSE')
		
		Grid.rowconfigure(self.window,0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)

		self.frame = Frame(self.window)
		self.frame.grid(row=0, column=0, sticky=N+S+E+W)
		Grid.columnconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 1, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.rowconfigure(self.frame, 1, weight=1)
	
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
			#self.save_config()
			exit()

	#loading config by json file
	def loading_config(self):
		try: 
			self.config.update(load_configure("COC/config/config.json"))
			self.d = self._config['d']
		except Exception as e:
			raise e
			messagebox.showinfo("Error", "configure error")
			exit()

	#Saving the config into the file config.json
	def save_config(self):
		with open('COC/config/config.json', 'w',encoding='utf-8') as outfile:
				json.dump(self.config, outfile, ensure_ascii=False, indent=4, sort_keys=True)
