#!/usr/bin/python3
import tkinter as tk
import psutil,sys
from tkinter import messagebox

class EMULATOR(tk.Frame):

	def __init__(self ,config, *args, **kwargs):
		#--------------------Windows-----------------------------------------
		self.config = config

		self.emus = self.find_emulator()

		if len(self.emus) == 0:
			messagebox.showinfo("Didn't find an emulatr", "Please start emulator first")
			exit()
		elif len(self.emus) == 1:
			self.config['pid'] = self.emus[0][1]
		else:
			self.window = tk.Tk()
			tk.Frame.__init__(self, self.window, *args, **kwargs)
			self.select_emu_GUI()

	def select_emu_GUI(self):
		n = len(self.emus)

		self.window.title("Select A Emulator")
		self.window.geometry("200x" + str(n*30))
		self.window.resizable(width = False, height = False)

		def set_devices(i):
			self.window.destroy()
			self.config['pid'] =  self.emus[i][1]

		for i in range(n):
			tk.Button(self.window, text = self.emus[i] ,anchor = "ne" ,width = 20,
			 command = lambda id=i:set_devices(id) ).grid(row=i,column=0)

		self.window.mainloop()

	def find_emulator(self):
		devices = list()
		Emulator = {'dnplayer':'雷电模拟器',
					'NemuPlayer':'网易MuMu',
					'BlueStacks':'蓝叠'
					}
		# show processes info
		pids = psutil.pids()
		try:
			for pid in pids:
				p = psutil.Process(pid)# get process name according to pid
				process_name = p.name()
				if process_name in Emulator.keys():
					if sys.platform == 'win32':
						handle  = p.num_handles()
						print("Process name is: %s, pid is: %s, num of handles : %s" %(process_name, pid, handle))
						devices.append([Emulator[process_name],handle])
					else:
						print("Process name is: %s, pid is: %s" %(process_name, pid))
						devices.append([Emulator[process_name],pid])
		except Exception as e:
			pass

		return devices