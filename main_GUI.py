#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
from COC.COC_GUI import *


class My_Bots(tk.Frame):

	def __init__(self, window, *args, **kwargs):
		tk.Frame.__init__(self, window, *args, **kwargs)
		#--------------------Windows-----------------------------------------
		self.window = window
		self.window.title("My Bots")
		self.window.geometry("300x"+ str(1*30))
		self.window.resizable(width = False, height = False) #fix window size

		#--------------------Games-------------------------------------------- 
		Button(self.window, text = "Clash of Clan",
				command = self.COC_Bot,anchor = W,width = 90).pack()

	def COC_Bot(self):
		self.window.destroy()
		coc = COC_GUI()
		coc.start()
		
	def start(self):
		self.window.mainloop()

def main():
	init_window = tk.Tk()
	Bot = My_Bots(init_window)
	Bot.start()

main()