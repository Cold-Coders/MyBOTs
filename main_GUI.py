#!/usr/bin/python3
import tkinter # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
from tkinter import *
from COC.GUI import *


class My_Bots():

	def __init__(self):
		#--------------------Windows-----------------------------------------
		self.window = Tk()
		self.window.title("My Bots")
		self.window.geometry("300x"+ str(1*30))
		self.window.resizable(width = False, height = False) #fix window size


		#--------------------Games-------------------------------------------- 
		Button(self.window, text = "Clash of Clan",
				command = self.COC_Bot,anchor = W,width = 90).pack()

		#---------------------MainLoop-----------------------------------------
		self.window.mainloop()

	def COC_Bot(self):
		self.window.destroy()
		GUI().start()

Bot = My_Bots()