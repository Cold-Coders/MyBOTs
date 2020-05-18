#!/usr/bin/python3
import tkinter as tk

def set_close(root,func = 'self'):
	if func == 'self':
		def close():
			root.destroy()
			exit()
		root.protocol("WM_DELETE_WINDOW", close)
	else:

		def close():
			func()
			root.destroy()
		root.protocol("WM_DELETE_WINDOW", close)