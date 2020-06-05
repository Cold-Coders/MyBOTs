#!/usr/bin/python3
import tkinter as tk
import PIL.Image
from PIL import ImageTk

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
