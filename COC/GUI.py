#!/usr/bin/python3
import tkinter # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
from tkinter import *

class GUI:
	def __init__(self):
		self.root = tkinter.Tk()
		# Code to add widgets will go here...
		self.SetUpMenu()
		
	def donothing(self):
		filewin = Toplevel(self.root)
		button = Button(filewin, text="Do nothing button")
		button.pack()

	def SetUpMenu(self):
		menubar = Menu(self.root)

		filemenu = Menu(menubar, tearoff = 0)
		filemenu.add_command(label="New", command = self.donothing)
		filemenu.add_command(label = "Open", command = self.donothing)
		filemenu.add_command(label = "Save", command = self.donothing)
		filemenu.add_command(label = "Save as...", command = self.donothing)
		filemenu.add_command(label = "Close", command = self.donothing)
		filemenu.add_separator()
		filemenu.add_command(label = "Exit", command = self.root.quit)
		menubar.add_cascade(label = "File", menu = filemenu)

		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label = "Undo", command = self.donothing)
		editmenu.add_separator()
		editmenu.add_command(label = "Cut", command = self.donothing)
		editmenu.add_command(label = "Copy", command = self.donothing)
		editmenu.add_command(label = "Paste", command = self.donothing)
		editmenu.add_command(label = "Delete", command = self.donothing)
		editmenu.add_command(label = "Select All", command = self.donothing)
		menubar.add_cascade(label = "Edit", menu = editmenu)

		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label = "Help Index", command = self.donothing)
		helpmenu.add_command(label = "About...", command = self.donothing)
		menubar.add_cascade(label = "Help", menu = helpmenu)

		self.root.config(menu = menubar)

	def start(self):
		self.root.mainloop()



bot = GUI()
bot.start()