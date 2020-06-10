from COC.Func.Others import Utils as U
from datetime import timedelta
import datetime

class Scenario:
	def __init__(self, GUI, coord, resolution):
		self.map = coord["Common"]['Map']
		self.path = 'COC/recognition/' + resolution + "/Common/"

		self.d = GUI._config['d']
		self.lang = GUI.lang['Common']

	def time_left(self,time : datetime.datetime):
		return (time - self.now()).total_seconds()

	def now(self):
		return datetime.datetime.now()

	def time(self,time):
		return time.strftime('%H:%M:%S')

	def duration(self, now = True , days = 0, minutes = 0, seconds = 0):
		if now == True:
			return (datetime.datetime.now() + timedelta(days = days, minutes = minutes, seconds = seconds))
		elif type(now) is datetime.datetime:
			return (now + timedelta(days = days, minutes = minutes, seconds = seconds))
	
	def Scense(self, screen, spec = 0,close = True, Debug = False):
		
		pos = { 
				1: 'townhall.png',
				2: 'builder.png',
				3: 'observe_townhall.png',
				4: 'search_townhall.png',
				5: 'search_builder.png',
				6: 'clan_chat.png',
				7: 'okay1.png',
				8: 'goldenpass_x.png',
				9: 'donation_x.png',
				10: 'clan_x.png'
		}

		
		close_list = [7,8,9,10]
		if spec == 0:
			for i in range(1,len(pos) + 1):
				x,y = ( U.find_PosbyArea(screen,self.map[ pos[i] ]\
					, self.path + pos[i] ,confidence = 0.95))
				if x > -1:
					if close and i in close_list:
						U.tap(self.d,x,y)
						U.prt(self.lang['msgs'][0],mode = 2)
					return i
			return 0 #未知场景

		
		area = self.map[ pos[spec] ]
		img = self.path + pos[spec]
		x,y = U.find_PosbyArea(screen,area, img,confidence = 0.95)
		if x > -1:
			if close and spec in close_list:
				U.tap(self.d,x,y)
			return True
		return False