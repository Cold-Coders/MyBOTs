#!/usr/bin/python3
import tkinter as tk
import PIL.Image
from PIL import ImageTk
from tkinter import ttk

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

def place_image(CLASS, frame: tk.Canvas,image,x,y,anchor = "nw",resize = 0):
	
	if not hasattr(CLASS,"extra_place_img"):
		CLASS.extra_place_img = []
	assert type(CLASS.extra_place_img) is list, "CLASS.extra_place_img is not list"

	if resize == 0:
		img = PIL.Image.open(image)
	else:
		img = PIL.Image.open(image).resize((resize[0], resize[1]))

	#会是当前这个对象里存在的最后一个图片
	CLASS.extra_place_img.append( ImageTk.PhotoImage(img) )
	frame.create_image(x,y,image=CLASS.extra_place_img[-1],anchor = anchor)

def place_label(CLASS, frame: tk.Canvas,x,y,anchor = "nw",bg = "white",\
				text = "", fg = "black" , relief = "flat",font = ""):
	
	if not hasattr(CLASS,"extra_place_label"):
		CLASS.extra_place_label = []
	assert type(CLASS.extra_place_label) is list, "CLASS.extra_place_label is not list"

	if font == "":
		CLASS.extra_place_label.append(tk.Label(frame, text = text, relief = relief ,\
		 background = bg, fg = fg , anchor = anchor))
	else:
		CLASS.extra_place_label.append(tk.Label(frame, text = text, relief = relief ,\
		 background = bg, fg = fg , anchor = anchor, font = font ))
	CLASS.extra_place_label[-1].place(x = x , y = y)

def place_selection(CLASS,frame, x, y, values = [], state="readonly" ,justify = 'center' , array = "extra",width = 10):
	if not hasattr(CLASS,"extra_place_selection"):
		CLASS.extra_place_selection = []
	
	assert type(CLASS.extra_place_selection) is list, "CLASS.extra_place_selection is not list"

	if array != "extra":
		CLASS.extra_place_selection.append( ttk.Combobox(frame,values=values,\
			width = width, justify = justify,state = state, textvariable = array))
	else:
		CLASS.extra_place_selection.append( ttk.Combobox(frame,values=values,\
			width = width, justify = justify,state = state))
	
	CLASS.extra_place_selection[-1].place(x = x , y = y)

def create_window(frame, window, x, y, anchor = 'nw'):
	frame.create_window(x,y, anchor= anchor , window=window)
