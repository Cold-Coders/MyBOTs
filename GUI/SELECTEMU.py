#!/usr/bin/python3
import tkinter as tk
import psutil,sys,os
from tkinter import messagebox
from GUI.GUI_utils import *

class EMULATOR(tk.Frame):

	def __init__(self ,config, *args, **kwargs):
		#--------------------Windows-----------------------------------------
		self.config = config

		self.emus = self.find_emulator()

		self.define_emus()
		#if len(self.emus) == 0:
		#	messagebox.showinfo("Didn't find an emulatr", "Please start emulator first")
		#	exit()		

		if len(self.emus) == 1:
			self.set_emu(0)

		elif len(self.emus) > 1:
			self.window = tk.Tk()
			tk.Frame.__init__(self, self.window, *args, **kwargs)
			self.select_emu_GUI()

	def define_emus(self):
		emus_dict = {}
		for i in range(len(self.emus)):
			name = self.emus[i][0]
			if name not in emus_dict:
				emus_dict[name] = 1
				self.emus[i][0] += "1"
			else:
				emus_dict[name] += 1
				self.emus[i][0] += str(emus_dict[name])

	def set_emu(self,i):
		self.config['emu'] = self.emus[i][0]
		self.config['pid'] = self.emus[i][1]
		if sys.platform == 'win32':
			self.config['handle'] = self.emus[i][2]
			self.config['path'] = self.emus[i][3]

	def select_emu_GUI(self):
		n = len(self.emus)

		self.window.title("Select A Emulator")
		self.window.geometry("300x" + str(n*30))
		self.window.resizable(width = False, height = False)
		self.window.grid_columnconfigure(0, weight=1)
		def set_devices(i):
			self.window.destroy()
			self.set_emu(i)

		for i in range(n):
			tk.Button(self.window, text = self.emus[i][0] ,anchor = "center" ,
			 command = lambda id=i:set_devices(id) ).grid(row=i,column=0, sticky='nesw')
		set_close(self.window)
		self.window.mainloop()

	def find_emulator(self):
		devices = list()
		Emulator = {'dnplayer.exe':'雷电模拟器',
					'NemuPlayer.exe':'网易MuMu',
					'NemuPlayer':'网易MuMu',
					'BlueStacks.exe':'蓝叠',
					"Nox.exe":'夜神'
					}
		# show processes info
		pids = psutil.pids()
		try:
			for pid in pids:
				p = psutil.Process(pid)# get process name according to pid
				process_name = p.name()
				if process_name in Emulator.keys():
					if sys.platform == 'win32':
						process_path = p.exe()
						process_path = process_path[:process_path.rfind("\\")]
						#print(process_path)
						handle  = p.num_handles()
						print("Process name is: %s, pid is: %s, num of handles : %s" %(process_name, pid, handle))
						devices.append([Emulator[process_name],pid,handle,process_path])
					else:
						print("Process name is: %s, pid is: %s" %(process_name, pid))
						devices.append([Emulator[process_name],pid])
		except Exception as e:
			raise e
			#exit()

		return devices