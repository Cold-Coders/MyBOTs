#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import json,os,time,threading,logging
import uiautomator2 as u2

from PIL import ImageTk
import PIL.Image

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from util import *

from GUI.GUI_logs import *
from GUI.GUI_utils import *

from COC.COC_Bot import COC_BOT
from COC.Func.Others import Utils as U
from COC.Func.Common import Scenario
from COC.Func.General import General
from COC.Func.Upgrade import Upgrade
from COC.Func.Donation import Donation
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

		#-------------------Initialize widget--------------------------------------
		self.build_basic_window()
		self.build_left_part()
		self.build_right_part()
		self.build_menu()
		set_close(self.window, func = self.save_config)
		#-------------------Initialize function--------------------------------------
		self.check_resolution()
		self.init_Func()
		

	def start(self):
		def BotRun():
			MyBot = COC_BOT(self._config,self.lang,self)
			MyBot.run()
			#while True:
			#	time.sleep(1)

		info_update = threading.Thread(target=BotRun, args=[])
		info_update.daemon = True
		info_update.start()

		self.window.mainloop()

	def init_Func(self):
		h,w = self.d.window_size()
		resolution = str(w) + "x" + str(h)
		coord = load_configure("COC/config/" + resolution + ".json")
		self._config["Common"] = Scenario(coord)
		self._config["General"] = General(self,resolution,coord)
		self._config["Upgrade"] = Upgrade(self,resolution)
		self._config["Donation"] = Donation(self,resolution)

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

		menubar = Menu(self.window)
		text = self.lang["menu"]

		def donothing():
		   filewin = Toplevel(self.window)
		   button = Button(filewin, text="Do nothing button")
		   button.pack()

		#-------------------Bots Setting--------------------------------------
		BOTMenu = Menu(menubar, tearoff=0)
		def init_U2():
			os.system("python -m uiautomator2 init")
		BOTMenu.add_command(label=text["initial"], command=init_U2)
		def re_connect_u2():
			self._config['d'] = u2.connect( self._config['device'] )
			self.d = self._config['d']
		BOTMenu.add_command(label=text["reconnect"], command=re_connect_u2)
		BOTMenu.add_separator()
		BOTMenu.add_command(label=text["Exit"], command=self.window.quit)

		#-------------------General Setting--------------------------------------
		GenMenu = Menu(menubar, tearoff=0)

		GenMenu.add_command(label=text["common"],
				command=lambda : self._config["General"].set_general(self.window))
		GenMenu.add_command(label=text["donation"], 
				command=lambda : self._config["Donation"].set_donation(self.window))
		#GenMenu.add_command(label=text["common"], command=donothing)
		
		

		#-------------------Menubar widget--------------------------------------
		menubar.add_cascade(label=text["setting"], menu=BOTMenu)
		menubar.add_cascade(label=text["general"], menu=GenMenu)
		self.window.config(menu=menubar)


	def build_right_part(self):
		self.right_part = Canvas(self.window,bg = "white",width=400,height=800)
		self.right_part.grid(row = 0, column = 1 ,rowspan = 2, sticky=N+S+E+W)
		self.set_information()
		self.set_function()
		self.test_area()

		place_image(self,self.right_part,"COC/res/dragon.png",150,300)

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
			self.img_list = list()
			if not sys.platform == 'win32':
				find_img = "ls | grep '.png'"
			else:
				find_img = 'dir|findstr ".png"'
	
			stream = os.popen(find_img)
			imgs = stream.read().split()
			for img in imgs:
				if ".png" == img.strip()[-4:]:
					self.img_list.append(img)

			self.testfind = ttk.Combobox(self.right_part,values=self.img_list)
			self.right_part.create_window(30 , 560 + 4 *40 + 10, anchor= NW , window=self.testfind)

		#Zoom out
		self.test_button[0]['command']= lambda: U.zoom_out(self.d)
		#Screen shot
		self.shot_mode = tk.IntVar()
		self.shot_color = tk.IntVar()
		def get_cords():
			cord = list()
			for corp in self.corps:
				num = corp.get()
				try:
					num = int(num)
				except Exception as e:
					U.prt(self.lang['tips']['coordinate_error'],mode = 3)
					return
					#raise e
				cord.append(num)

			area = tuple(cord)
			return area

		def new_shot():
			mode = self.shot_mode.get()
			color = self.shot_color.get()
			# 0 color 1 gray self.shot_color
			if mode == 1:
				Screen = U.crop_screen(self.d.screenshot(format="opencv"),get_cords())
			elif  mode == 0:
				Screen = self.d
			if color == 0:
				U.save_screen(Screen)
			elif color == 1:
				U.save_screen(Screen,gray = True)

			search_imgs()

		self.test_button[1]['command']= lambda: new_shot()
		#Recognize information
		self.test_button[2]['command']= lambda: self._config["General"].Update_info()
		#Collect resourse
		self.test_button[3]['command']= lambda: self._config["General"].collect_resourse()
		#Remove obstacle once
		self.test_button[4]['command']= lambda: self._config["General"].remove_single_obstacle()
		#Test crop Area
		self.test_button[5]['command']= lambda: U.test_crop(self.d,get_cords())
		#Test donation
		self.test_button[6]['command']= lambda: self._config["Donation"].donateOnce()
		#Test IMAGE
		self.test_button[7]['command']= lambda: U.Image_Test(self.d)
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

		#--------------------------Screen Shot by Area-----------------------------------------------------
		tk.Label(self.right_part,text = "x1", relief="flat", background = "white").place(x = 30, y = 680)
		tk.Label(self.right_part,text = "y1", relief="flat", background = "white").place(x = 30, y = 700)
		tk.Label(self.right_part,text = "x2", relief="flat", background = "white").place(x = 100, y = 680)
		tk.Label(self.right_part,text = "y2", relief="flat", background = "white").place(x = 100, y = 700)
		self.corps = [tk.Entry(width = 5),tk.Entry(width = 5),tk.Entry(width = 5),tk.Entry(width = 5)]
		self.right_part.create_window(50 , 680, anchor= NW , window=self.corps[0])
		self.right_part.create_window(50 , 680 + 20, anchor= NW , window=self.corps[1])
		self.right_part.create_window(120 , 680, anchor= NW , window=self.corps[2])
		self.right_part.create_window(120 , 680  + 20, anchor= NW , window=self.corps[3])
		tk.Radiobutton(self.right_part,text = 'Color', relief="flat", background = "white",
						value=0, var=self.shot_color).place(x = 175, y = 680)
		tk.Radiobutton(self.right_part,text = 'Gray', relief="flat", background = "white" ,
						value=1, var=self.shot_color).place(x = 175, y = 700)
		tk.Radiobutton(self.right_part,text = self.lang['titles']['full'], relief="flat", background = "white",
						value=0, var=self.shot_mode).place(x = 245, y = 680)
		tk.Radiobutton(self.right_part,text = self.lang['titles']['partial'], relief="flat", background = "white" ,
						value=1, var=self.shot_mode).place(x = 245, y = 700)

	def set_function(self):
		self.right_part.create_text(65,200,text = self.lang['func_Area'], fill="darkblue",font="Times 20 italic bold")

		self.func = list()
		for i in range(len(self.lang['func_name'])):
			self.func.append(BooleanVar(value = self.config['Functionality'][i]))
			donate = Checkbutton(self.right_part, text = self.lang['func_name'][i],
				variable = self.func[i],bg="white", offvalue = 0, height = 1, width = 10)
			donate.place(x = 20, y = 230 + i*30)

	def set_information(self):
		#------------------------background-----------------------------------------------
		# self.img2 = tk.PhotoImage(file= "COC/res/elixir.png")
		# canva.create_image(20,20,image=self.img2,anchor =NW)
		#------------------------Information Board-------------------------
		self.right_part.create_text(75,15,text = "游戏状态", fill="darkblue",font="Times 20 italic bold")
		fill_color = [
					  "brown",
					  "red",
					  "Green"
					 ]
		self.homevillage_img = list()
		self.info_text = list()
		self.list_info_widget = list()

		for i in range(len(self.config['HomeVillage_image'])):
			#self.right_part.create_text(110,50 + 40*i,text = self.lang['info_name'][i],fill = fill_color[i%len(fill_color)])
			
			label = tk.Label(self.right_part, text = "0", relief="flat", background = "white", \
						fg = fill_color[i%len(fill_color)])
			label.place(x = 60 + 140*int(i//3) , y = 60 + 40*(i%3) )
			self.info_text.append(label)

			image = PIL.Image.open(self.config['HomeVillage_image'][i]).resize((40, 40))
			image = ImageTk.PhotoImage(image)
			self.homevillage_img.append(image)

			self.list_info_widget.append( self.right_part.create_image(20 + 135*int(i/3) ,50 + 40 * (i%3),
								 image = self.homevillage_img[i], anchor = NW) )
		
		self.builder_img = list()
		for i in range( len(self.config['BuilderBase_image']) ):
			img = PIL.Image.open(self.config['BuilderBase_image'][i]).resize((40, 40))
			img = ImageTk.PhotoImage(img)
			self.builder_img.append(img)


		#改变提示为建筑大师资源 和 家乡基地
		self.info_title = StringVar()
		self.info_title.set(self.lang["titles"]["HomeVillage"])
		tk.Label(self.right_part, textvariable = self.info_title,
					relief="flat", background = "white", fg="blue").place(x = 60, y = 30)
		
		tk.Label(self.right_part, text = self.lang["titles"]["Cumulative"],
					relief="flat", background = "white", fg="blue").place(x = 200, y = 30)

		tk.Label(self.right_part, text = self.lang["titles"]["Others"],
					relief="flat", background = "white", fg="blue").place(x = 320, y = 30)
		#self.right_part.itemconfig(self.list_info_widget[2],image = self.list_info_pic[0])



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
			messagebox.showinfo("Error", "language profile error")
			print(e)
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
	def init_config(self):
		self.config = {
			"BuilderBase_image": [
				"COC/res/gold.png",
				"COC/res/elixir.png",
				"COC/res/gem.png"
			],
			"Functionality": [
				False,
				False,
				False,
				False
			],
			"HomeVillage_image": [
				"COC/res/gold.png",
				"COC/res/elixir.png",
				"COC/res/dark_elixir.png",
				"COC/res/gold_storage.png",
				"COC/res/elixir_storage.png",
				"COC/res/dark_storage.png",
				"COC/res/Builder_info.png",
				"COC/res/Master_Builder_info.png",
				"COC/res/wait.png"
			],
			"coc_icon": "COC/res/coc_icon.png",
			"coc_logo": "COC/res/COC_logo.png",
			"lang": "chn",
			"orc": 2,
			"resource": "COC/res/resource.png"
		}

	#Saving the config into the file config.json
	def save_config(self):
		for i in range(len(self.func)):
			self.config['Functionality'][i] = self.func[i].get()
		with open('COC/config/config.json', 'w',encoding='utf-8') as outfile:
				json.dump(self.config, outfile, ensure_ascii=False, indent=4, sort_keys=True)