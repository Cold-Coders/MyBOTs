from  PIL import  Image
import pytesseract
import  cv2 as cv
 
 
img_path='test.png'
 
# img_path='orgin.jpg'
 
# img_path='F:/fb/hpop.jpg'

tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'

# 依赖opencv
img=cv.imread(img_path)
text=pytesseract.image_to_string(Image.fromarray(img), config=tessdata_dir_config,lang = "chi_sim")
 
 
# 不依赖opencv写法
# text=pytesseract.image_to_string(Image.open(img_path))
 
 
print(text)