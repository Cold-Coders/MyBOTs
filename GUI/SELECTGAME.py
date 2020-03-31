#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox

class SELECTGAME(tk.Frame):

	def __init__(self ,config, *args, **kwargs):
		self.GameList = {'com.supercell.clashofclans.guopan': "部落冲突 果盘版",
						'com.tencent.tmgp.rxcq':"热血传奇 腾讯",
						'com.supercell.clashofclans':"部落冲突 Google"
			}

		self.config = config
		self.d = config['d']
		self.games = self.find_a_game()

		if len(self.games) == 0:
			messagebox.showinfo("Didn't find an available game", "We are available for \
				 \n 1. Clash of clan\
				 \n 2. MIR mobile from Tencent")
			exit()
		elif len(self.games) == 1:
			self.config['game'] = self.games[0]
		else:
			self.window = tk.Tk()
			tk.Frame.__init__(self, self.window, *args, **kwargs)
			self.select_a_game()
				
	def select_a_game(self):
		n = len(self.games)

		self.window.title("Select A Game")
		self.window.geometry("200x" + str(n*30))
		self.window.resizable(width = False, height = False)

		def set_devices(i):
			self.window.destroy()
			self.config['game'] =  self.games[i]

		for i in range(n):
			tk.Button(self.window, text = self.GameList[self.games[i]] ,anchor = "ne" ,width = 20,
			 command = lambda id=i:set_devices(id) ).grid(row=i,column=0)

		self.window.mainloop()

	def find_a_game(self):
		running = self.d.app_list_running()
		
		available = list()
		for app in running:
			if app in self.GameList.keys():
				available.append(app)

		return available
