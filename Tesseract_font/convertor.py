import cv2,sys,os

img_list = list()
if not sys.platform == 'win32':
	find_img = "ls | grep '.png'"
else:
	find_img = 'dir|findstr ".png"'
	
stream = os.popen(find_img)
imgs = stream.read().split()
for img in imgs:
	if ".png" == img.strip()[-4:]:
		img_list.append(img)

count = 0
for img in img_list:
	res = cv2.imread(img)
	cv2.imwrite(str(count) + ".tif",res)
	count += 1
	os.remove(img)