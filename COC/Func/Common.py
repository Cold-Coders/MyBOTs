from COC.Func.Others import Utils as U
from datetime import timedelta
import datetime

class Scenario:
	def __init__(self, coord, resolution):
		self.map = coord["Common"]['Map']
		self.path = 'COC/recognition/' + resolution + "/Common/"

	def time_left(self,time : datetime.datetime):
		return (time - self.now()).total_seconds()

	def now(self):
		return datetime.datetime.now()

	def time(self,time):
		return time.strftime('%H:%M:%S')

	def duration(self, now = datetime.datetime.now() , days = 0, minutes = 0, seconds = 0):
		return (now + timedelta(days = days, minutes = minutes, seconds = seconds))

	def Scense(self, screen, spec = 0, Debug = False):
		
		pos = { 
				1: 'townhall.png',
				2: 'builder.png',
				3: 'observe_townhall.png',
				4: 'search_townhall.png',
				5: 'search_builder.png',
				6: 'clan_chat.png'
		}

		

		if spec == 0:
			for i in range(1,len(pos) + 1):
				if ( U.find_PosbyArea(screen,self.map[ pos[i] ]\
					, self.path + pos[i] ,confidence = 0.95))[0] > -1:
					return i
			return 0 #未知场景

		
		area = self.map[ pos[spec] ]
		img = self.path + pos[spec]
		if ( U.find_PosbyArea(screen,area, img,\
			confidence = 0.95))[0] > -1:
			return True
		return False