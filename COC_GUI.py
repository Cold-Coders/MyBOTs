#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import json,os,time,threading,logging
import tkinter.scrolledtext as ScrolledText

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


	def build_gui(self):                    
		# Build GUI
		self.window.title("My CoC Bots")
		self.window.resizable(width = False, height = False)
		self.window.geometry("900x600") #wxh
		self.window.option_add('*tearOff', 'FALSE')
		self.grid(column=0, row=0, sticky='ew')
		self.grid_columnconfigure(0, weight=1, uniform='a')
		self.grid_columnconfigure(1, weight=1, uniform='a')
		self.grid_columnconfigure(2, weight=1, uniform='a')
		self.grid_columnconfigure(3, weight=1, uniform='a')

		# Add text widget to display logging info
		st = ScrolledText.ScrolledText(self, state='disabled')
		st.configure(font='TkFixedFont')
		st.grid(column=0, row=1, sticky='w', columnspan=4)

		# Create textLogger
		text_handler = TextHandler(st)

		# Logging configuration
		logging.basicConfig(filename='test.log',
			level=logging.INFO, 
			format='%(asctime)s - %(levelname)s - %(message)s')        

		# Add the handler to logger
		logger = logging.getLogger()        
		logger.addHandler(text_handler)
	
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
	