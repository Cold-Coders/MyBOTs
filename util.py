import time,json,os,sys,re

def r_color(c1,c2,diff = 8):
    if type(c1) is tuple and type(c2) is tuple :
      return abs(c1[0] - c2[0]) <= diff and abs(c1[1] - c2[1])  <= diff and abs(c1[1] - c2[1]) <= diff
    elif type(c1) is int and type(c2) is int:
      return abs(c1 - c2) <= diff
    elif len(c1) == 3 and len(c2) == 3:
      return abs(c1[0] - c2[0]) <= diff and abs(c1[1] - c2[1])  <= diff and abs(c1[1] - c2[1]) <= diff

def ss(t = 0.1):
	time.sleep(t)

def load_configure(file: str,resolution:str):
    f=open(file,encoding='utf-8')
    content=f.read()
    res=json.loads(content)
    prt(res[resolution])
    return(res[resolution])
    
def msg(*message):
	s = ""
	for m in message:
		s += str(m) + " "
	print("[%s]"%time.asctime(),s)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def prt(*args):
	print("\nDebug" + ">"*45 )
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

# print dict 
def print_d(res,tab = ''):
    for key in res.keys():
    	if type(res[key]) is dict:
    		print(key,":")
    		print_d(res[key],'\t')
    	else:
        	print(tab,key,":",res[key])