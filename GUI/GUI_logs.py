import time
import threading
import logging
try:
	import tkinter as tk # Python 3.x
	import tkinter.scrolledtext as ScrolledText
except ImportError:
	import Tkinter as tk # Python 2.x
	import ScrolledText

class MyLogUi:
	def __init__(self,frame,bg = "black",fg = "white",height = 50):
		# Add text widget to display logging info
		self.st = ScrolledText.ScrolledText(frame, state='disabled',
					bg = bg, fg = fg, height = height)
		self.st.configure(font='TkFixedFont')
		self.st.tag_config('INFO', foreground='white')
		self.st.tag_config('DEBUG', foreground='green')
		self.st.tag_config('WARNING', foreground='orange')
		self.st.tag_config('ERROR', foreground='red')
		self.st.tag_config('CRITICAL', foreground='red', underline=1)

		# Create textLogger
		text_handler = TextHandler(self.st)

		# Logging configuration
		logging.basicConfig(filename='test.log',
			level=logging.INFO, 
			format='%(asctime)s - %(levelname)s - %(message)s')        

		#Add the handler to logger
		logger = logging.getLogger()        
		logger.addHandler(text_handler)

	def place(self,x,y):
		self.st.place(x, y)

	def grid(self,row,column,strick = "nsew", rowspan = 1, columnspan = 1):
		self.st.grid(row = 1, column = 0, sticky="nsew")

class TextHandler(logging.Handler):
	# This class allows you to log to a Tkinter Text or ScrolledText widget
	# Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

	def __init__(self, text):
		# run the regular Handler __init__
		logging.Handler.__init__(self)
		# Store a reference to the Text it will log to
		self.text = text

	def emit(self, record):
		msg = self.format(record)
		def append():
			# Autoscroll to the bottom
			self.text.configure(state='normal')
			self.text.insert(tk.END, msg + '\n',record.levelname)
			self.text.configure(state='disabled')
			# Autoscroll to the bottom
			self.text.yview(tk.END)
		# This is necessary because we can't modify the Text from other threads
		self.text.after(0, append)

def show_log(msg,mode = 1):
	timeStr = time.asctime()
	msg = timeStr + ": " + msg
	#values = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
	if mode == 0:
		logging.log(10,msg)
	elif mode == 1:
		logging.info(msg)
	elif mode == 2:
		logging.warning(msg)
	elif mode == 3:
		logging.error(msg)
	elif mode == 4:
		logging.critical(msg)