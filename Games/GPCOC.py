import unittest
import uiautomator2 as u2
from util import *
from cv import CV
from Constant import *
#from appium import webdriver

class GP_COC:
    def __init__(self, device = "",ver = 1,mode = 'a'):
        self._DEBUG = True
        self.d = u2.connect(device)
        self._mode = mode # a - 辅助模式 f - 全模式 gp-果盘只进入游戏

        V = ['com.supercell.clashofclans.guopan',
             'com.tencent.tmgp.supercell.clashofclans']
        self._app = V[ver]
        
        self.coordinate = []
        self.dWidth, self.dHeight = self.d.window_size() 
        resol = str(self.dWidth) + "x" + str(self.dHeight)
        self.coord = load_configure("Games/Coc.json",resol)

        self.config = load_configure("Games/GameConfig.json","COC")


    def dectect_app(self):
        pid = self.d.app_wait(self._app) # 等待应用运行, return pid(int)

        if self._DEBUG:
            if not pid:
                print(self._app,"is not running")
            else:
                print(self._app,"pid is %d" % pid)
        return pid

    def LaunchCOC(self):
        self.d.app_start(self._app)

    def StopCOC(self):
        self.d.app_stop(self._app) 

    def GPEG(self):
        COUNT  = dict()

        EXISTS = lambda a,b: self.d(text=a, className=b).exists()
        CLICK = lambda a,b: self.d(text=a, className=b).click()
        try:
            #是否运行游戏 并 存在Textview的文字为进入游戏
            if self.dectect_app() and EXISTS("进入游戏",TEXTVIEW):
                CLICK("进入游戏",TEXTVIEW)
                COUNT[EnterGame] += 1 
                prt("点击进入游戏次数",COUNT[EnterGame])
            #睡眠100秒
            ss(100)
        except(Exception):
            #睡眠5分钟当有其他操作
            ss(60*5)

    def _srcv(self):
        return self.d.screenshot(format="opencv")

    def _tap(self,sx,sy,r = False):
        try:
            if r:
                self.d.click(random.randint(1,sx), random.randint(1,sy))
            else:
                self.d.click(sx, sy)
            ss(random.randint(1,5) * 0.1)
        except(Exception):
            ss()

    def donate3(self, Text):
        D_List = self.config["Donation"]["List"]
        T_Img = self.coord['Donation']['troop']

        CHOP = lambda: CV.Crop(self._srcv(),self.coord['Donation']['d_rec'])
        w = self.coord['Donation']['d_rec'][0]
        h = self.coord['Donation']['d_rec'][1]

        def CLICK(a,b,c):
            msg("找到",a,"点击",b,",",c) 
            self._tap(b,c)
            ss(0.5)

        if '随' in Text:
            for do in D_List:
                target = T_Img[do]
                #print(target)
                x,y = CV.Match(CHOP(),target)
                if not (x==-1 or y == -1):
                    CLICK(target,x+w,y+h)

        #提取所需捐赠兵种
        To_D = list()
        for do in D_List:
            if do in Text:
                To_D.append(do)

        #依次点击要捐赠的兵种
        for do in To_D:
            if do in T_Img:
                target = T_Img[do]
                #print(target)
                x,y = CV.Match(CHOP(),target)
                if not (x==-1 or y == -1):
                    CLICK(target,x+w,y+h)
                    

    def donate2(self):
        #截取聊天框
        ss(1)
        
        w = self.coord['Donation']['crop']
        img_rgb = CV.Crop(self._srcv(),[0,0,w,self.dWidth])
        target = self.coord['Donation']['button']
        #找到捐赠按钮
        p_b = CV.find(img_rgb,target)
        #prt(p_b)
        
        #分割文字
        for i in range(len(p_b)):
            tx1,tx2 = self.coord['Donation']['text']
            ty1 = p_b[i][1] - 57
            ty2 = ty1 + 30
            TextImg = CV.Crop(img_rgb,[tx1,ty1,tx2,ty2])

            #ORC文字
            Text = CV.BdOrc(TextImg)

            print("执行",i,":",Text)
            self._tap(p_b[i][0],p_b[i][1])

            #捐兵步骤
            self.donate3(Text)

            #随机点击关闭捐赠界面
            self._tap(225, 332)
            ss(3)

        
        
        #关闭聊天框
        x,y = self.coord['Donation']['close']
        self._tap(x,y)

    def donate(self):
        #没有开启捐兵
        if not self.config["Donation"]["Enable"]:
            return
        #等级处是否为蓝色 为主界面
        img = self._srcv()
        x,y = self.coord['Donation']['colorCoor']
        c = CV.getPixel(img,x,y)
        cb = self.coord['Donation']['blue']
        cg = self.coord['Donation']['grey']
        #print(c,cc,type(c),type(cc))
        #主界面操作
        if r_color(c,cb):
            #打开聊天框
            x,y = self.coord['Donation']['open']
            self._tap(x,y)
            self.donate2()
        elif r_color(c,cg):#颜色判断是否在聊天界面
            self.donate2()
        else:
            msg(c,cb,type(c),type(cb),"未知错误")
            self._tap(555,555,r = True)

    def run(self):
        if self._DEBUG:
            self.donate()
            #CV.Save(self.d)
            #self.donate3("随意")
            #return
        while True:

            if 'com.supercell.clashofclans.guopan' == self._app:
                    self.GPEG()

            if self._mode == 'a':
                #收资源
                
                #捐兵
                self.donate()

                #造兵
            elif self._mode = 'gp':
                continue

            elif self._mode == 'f':
                #资源收集
                
                #造兵检测
                
                #捐兵检测
                self.donate()

                #出兵检测
                
                #升级检测
                
                #夜世界
                
                #夜世界升级检测
                
                #夜世界出兵

    

class Android_GP_COC(unittest.TestCase):

    # Before Test
    def setUp(self):
        desired_caps = {'platformName': 'Android', 
                        'platformVersion': '5.1.1',
                        'deviceName': 'emulator-5554',
                        'appPackage': 'com.supercell.clashofclans.guopan', 
                        'appActivity': 'com.supercell.clashofclans.guopan/com.supercell.titan.kunlun.GameAppKunlun',
                        'automationName':'UiAutomator2'
                        }
        #self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps) 
        #self.driver.implicitly_wait(8)
        self.runner = GP_COC()

    def Start_Test(self):
        ss(1)
        self.runner.run()
        ss(1)

    # After Test
    def tearDown(self):
        pass

