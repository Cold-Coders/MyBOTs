import time,json,os,sys,re,random

def r_num(seed = -1, rand = 1, ubound = 10,lbound = 0):
	if seed != -1:
		random.seed(seed)	
	else:
		random.seed( int(time.time() % 100) )
	if rand == 1:
		return random.randint(lbound,ubound)
	else:
		return [random.randint(lbound,ubound) for i in rand]


# args[0] 总次数, args[1] 每次间隔多少秒, percent 显示的格式
def ss(*args,precent = 0):
	if len(args) == 1 and args[0] > 0:
		#print("delay",args[0])
		time.sleep(args[0])
	elif len(args) == 2 and args[0] > 0 and args[1] > 0:
		if type(args[0]) is not int:
			msg("错误参数",args[0])
			return

		#args[0] is n times, args[1] is m sec interval
		for i in range(1,args[0] + 1):
			time.sleep(args[1])
			sec = args[1]*args[0]
			if percent == 0:
				print("休眠 {0:f} 秒.".format(sec,prec))
			elif precent == 1:
				prec = (i/args[0]*100)
				print("休眠 {0:f} 秒, {1:.1f} %".format(sec,prec), end="\r")
			elif precent == 2:
				p = int(i/args[0]*50)
				sp = p*'|'
				print("休眠 {0} 秒, {1:<55}{2:.1f}%".format(sec,sp,p*2), end="\r")
			else:
				print("休眠",args[1]*args[0],'秒, 第',i,'秒。', end="\r")
	else:
		time.sleep(0.1)
	
	

def load_configure(file: str,specific = ''):
	f=open(file,encoding='utf-8')
	content=f.read()
	res=json.loads(content)

	if not specific == '': 
		prt(res[specific])
		return(res[specific])
	else:
		return res
	
def msg(*message):
	s = ""
	for m in message:
		s += str(m) + " "
	print("[%s]"%time.asctime(),s)

def get_file_content(filePath):
	with open(filePath, 'rb') as fp:
		return fp.read()

# print dict 
def print_d(res,tab = ''):
	for key in res.keys():
		if type(res[key]) is dict:
			print(key,":")
			print_d(res[key],'\t')
		else:
			print(tab,key,":",res[key])

def prt(*args,title = "Debug",end = " "):
	print("\n"+ title + ">"*65 )
	skip = False
	for i in range(len(args)):
		#print(type(args[i]))

		if type(args[i]) is dict:
			print_d(args[i])

		elif type(args[i]) is list:
			for element in args[i]:
				print(element,end = end)
				
		#变量前为False就是跳过不显示
		elif type(args[i]) is bool:
			if not args[i]:
				skip = True
		elif skip:
			skip = False
			continue;

		else:
			print(args[i],end = end)

		print()
	print("<"*(len(title) + 65))
	print()

