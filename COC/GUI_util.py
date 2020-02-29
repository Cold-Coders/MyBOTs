#!/usr/bin/python3
import tkinter
import psutil
import os
import signal
import sys



def get_platform():
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

global Win
Win = True if get_platform() == 'Windows' else False
if Win:
	import win32gui

class Pre_GUI:
	
	@staticmethod
	def get_window_info():  # 获取阴阳师窗口信息
	    wdname = u'雷电模拟器'
	    handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄
	    if handle == 0:
	        # text.insert('end', '小轩提示：请打开PC端阴阳师\n')
	        # text.see('end')  # 自动显示底部
	        return None
	    else:
	        return win32gui.GetWindowRect(handle)
	
	@staticmethod
	def find_emulator():
		devices = list()

		Emulator = {'dnplayer.exe':'雷电模拟器',
					'NemuPlayer':'MacOs网易MuMu'
					}
		# show processes info
		pids = psutil.pids()

		for pid in pids:
		    p = psutil.Process(pid)
		    # get process name according to pid
		    process_name = p.name()
		    if process_name in Emulator.keys():
		    	if Win:
		    		handle  = p.num_handles()
		    		print("Process name is: %s, pid is: %s, num of handles : %s" %(process_name, pid, handle))
		    		devices.append((Emulator[process_name],process_name,pid,handle))
		    	else:
		    		print("Process name is: %s, pid is: %s" %(process_name, pid))
		    		devices.append((Emulator[process_name],process_name,pid))

		#out=os.system('netstat -aon|findstr "25"')#25端口号
		#print(out)#输出进程
		#out=os.system('tasklist|findstr "3316"')#3316进是程
		
		return devices

    
def Selection_Windows(title,L:list,width = '300'):
	def close():
			window.destroy()
			exit()

	window = tkinter.Tk()
	window.title(title)
	window.geometry(width + "x" + str(len(L)*30))
	window.resizable(width = False, height = False)
	window.protocol("WM_DELETE_WINDOW", close)
	return window