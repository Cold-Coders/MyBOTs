import aircv as ac
import uiautomator2

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from GUI.GUI_logs import *
from COC.Func.Others import Utils as U

from util import *

class Donation:
	def __init__(self, d , config , lang , resolution):
		self.d = d
		self.orc = config['orc']
		self.lang = lang
		
		path = 'COC/recognition/' + resolution + "/Resource/"

		Area = {
					"860x732":{
								"chat_box":   (0,0,310,732)
							  }
		}
		self.Area = Area[resolution]

		buttons = {
					"860x732":{
								"remove_obstacle": (427,630)
							  }
		}
		self.buttons = buttons[resolution]


		if 'General' not in config:
			self.config = {

			}
		else:
			self.config = config['General']