from COC.Func.Others import Utils as U

class Scenario:
	def __init__(self, coord):
		self.common_coord = coord["Common"]

	def Scense(self, screen, spec = 0, Debug = False):
		
		pos = { 
				1: self.common_coord['homebase'],
				2: self.common_coord['builder']
		}

		colors = dict()
		# 1 homebase
		colors[1] = [ 
					(255, 254, 228), #等级下面的降杯浅色部分
					(45, 113, 182), #护盾蓝色i
					(255, 234, 38), #进攻地图浅色部分
					(61, 49, 61) #黑水的黑色
				]
		# 2 builder
		colors[2] = [ 
					(255, 234, 198), #等级下面的降杯浅色部分
					(45, 113, 182), #护盾蓝色i
					(119, 133, 149), #进攻地图斧头的颜色
					(207, 238, 120) #宝石的颜色
				] 

		if spec == 0:
			for i in range(1,len(colors) + 1):
				count = 0
				for j in range(len(pos)):
					if not U.isColor(screen, pos[i][j], colors[i][j] ,diff = 10, Debug = Debug):
						break
					count += 1
				if count == len(colors[i]):
					return i
			return 0 #未知场景
		else:
			for i in range(len(pos[spec])):
				if not U.isColor(screen, pos[spec][i], colors[spec][i] ,diff = 10, Debug = Debug):
					if Debug:
						continue
					return False
			return True