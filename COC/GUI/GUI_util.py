#!/usr/bin/python3
import tkinter as tk
import psutil
import os
import signal
import sys
import subprocess
from util import *


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


class GUI_Tools:

	@staticmethod
	def set_close(root):
		def close():
			root.destroy()
			exit()
		root.protocol("WM_DELETE_WINDOW", close)

	@staticmethod
	def clr(root):
		for widget in root.winfo_children():
			widget.destroy()

	@staticmethod
	def selection(window:tk.Frame, title , L ,width = '300'):
		
		if type(width) is int:
			width = str(width)

		GUI_Tools.clr(window)
		window.title(title)
		window.geometry(width + "x" + str(len(L)*30))
		window.resizable(width = False, height = False)
		GUI_Tools.set_close(window)

		btns = list()
		if type(L) is dict:
			L = L.keys()

		for e in L:
			btn = tk.Button(window, text = e ,anchor = "ne" ,width = 90)
			btns.append(btn)
			btn.pack()

		return btns


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
	def devices(r = False):
		restart = 'adb kill-server && adb start-server'
		get_devices = 'adb devices'
		if Win:
			restart = restart.replace("adb","adb\\adb")
			get_devices = get_devices.replace("adb","adb\\adb")
		if r:
			os.system(restart)
		devices_adb = subprocess.check_output(get_devices, shell=True)
		devices_adb = devices_adb.decode("utf-8")
		devices_adb = devices_adb.replace("List of devices attached","")
		devices_adb = devices_adb.strip().split()

		#port=os.system('netstat -aon|findstr "555"')#25端口号
		#out=os.system('tasklist|findstr "3316"')#3316进是程
		
		devices = list()
		for i in range(0,len(devices_adb),2):
			if devices_adb[i + 1] != "offline":
				devices.append( devices_adb[i] )

		return devices
	
	