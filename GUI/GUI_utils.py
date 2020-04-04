#!/usr/bin/python3
import tkinter as tk

def set_close(root):
	def close():
		root.destroy()
		exit()
	root.protocol("WM_DELETE_WINDOW", close)