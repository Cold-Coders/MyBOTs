import os,sys
import uiautomator2 as u2

from util import *
from tkinter import messagebox
from GUI.SELECTADEVICE import DEVICE
from GUI.SELECTEMU import EMULATOR

class Emu_restarter:

	@staticmethod
	def Emu(config,lang):
		if sys.platform == 'win32':
			emu = config[ "emu" ]
			path = config['path']

			index = int(emu[-1] ) - 1
			emu =  emu[:-1] 
		
			cmds = { "雷电模拟器": 
						[ 	path + "\\dnconsole.exe quit --index " + str(index),
							path + "\\dnconsole.exe modify --index " + str(index) + " --resolution 860,732,160",
							path + "\\dnconsole.exe launch --index " + str(index)],
					"夜神":
						[ 	path + "\\dnconsole.exe quit --index " + str(index),
							path + "\\dnconsole.exe modify --index " + str(index) + " --resolution 860,732,160",
							path + "\\dnconsole.exe launch --index " + str(index)],
			
			}

			for cmd in cmds[emu]:
				print(cmd)
				os.system(cmd)
				ss(1)

			#wait 10s until start 
			messagebox.showinfo(lang["titles"]["restart"], lang["tips"]["re_connect_emu"])
			

			#re connect adb
			EMULATOR(config)

			DEVICE(config)

			#re-connect uiautomator2
			config['d'] = u2.connect( config['device'] )
			#dnconsole.exe quit --index 0
			#dnconsole.exe modify --index 0 --resolution 860,732,160
			#dnconsole.exe launch --index 0