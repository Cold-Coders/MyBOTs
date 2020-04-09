import os,sys,psutil
import uiautomator2 as u2
from COC.Func.Others import Utils as u

from util import *
from tkinter import messagebox
from GUI.SELECTADEVICE import DEVICE
from GUI.SELECTEMU import EMULATOR

class Emu_restarter:

	@staticmethod
	def Emu(config,lang):
		if not sys.platform == 'win32':
			messagebox.showinfo(lang["titles"]["restart"], lang["tips"]["not_support_emu"])
			exit()
		else:
			emu = config[ "emu" ]
			path = config['path']

			index = int(emu[-1] ) - 1
			emu =  emu[:-1] 
		
			cmds = { "雷电模拟器": 
						[ 	path + "\\dnconsole.exe quit --index " + str(index),
							path + "\\dnconsole.exe modify --index " + str(index) + " --resolution 860,732,160",
							path + "\\dnconsole.exe launch --index " + str(index)
						],
					"夜神":
						[ 	path + "\\Nox.exe -clone:Nox_" + str(index) + " -quit" ,
							path + "\\Nox.exe -clone:Nox_" + str(index) + " -resolution:860x732 -dpi:160",
							path + "\\Nox.exe -clone:Nox_" + str(index)
						]
			}

			if emu not in cmds:
				u.prt(lang["tips"]['not_support_emu'], mode = 3)
				messagebox.showinfo(lang["titles"]["restart"], lang["tips"]["not_support_emu"])
				exit()

			#before restart, save the activity name for later use
			acty = u.current_act(config['d'])

			for cmd in cmds[emu]:
				u.prt(cmd)
				os.popen(cmd)
				ss(2)

			u.prt(lang["tips"]["re_connect_emu"], mode = 2)
			#wait 10s until start 
			messagebox.showinfo(lang["titles"]["restart"], lang["tips"]["re_connect_emu"])

			#re connect adb
			EMULATOR(config)

			DEVICE(config)

			u.prt(lang["tips"]["re_connect_u2"], mode = 2)
			#re-connect uiautomator2
			config['d'] = u2.connect( config['device'] )

			u.prt(lang["tips"]["re_start_game"], mode = 2)
			#restart game
			config['d'].app_start(config['game'],acty)
			#dnconsole.exe quit --index 0
			#dnconsole.exe modify --index 0 --resolution 860,732,160
			#dnconsole.exe launch --index 0