import time

def ss(t = 0.1):
	time.sleep(t)

def msg(message):
    print("[%s]"%time.asctime(),message)

def prt(*args):
	skip = False
	for i in range(len(args)):
		if type(args[i]) is dict:
			print_d(args[i])
		elif type(args[i]) is bool:
			if not args[i]:
				skip = True
		elif skip:
			skip = False
			continue;
		else:
			print(args[i],end = " ")
		print()
	print("<"*50)
	print()