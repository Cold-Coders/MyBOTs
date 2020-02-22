import unittest
import uiautomator2 as u2
from util import *
from cv import CV
from Constant import *
import threading

#from appium import webdriver

class GP_COC:
    def __init__(self, device = "",ver = 1,mode = 'a'):
        self._DEBUG = False
        self.d = u2.connect(device)
        self._mode = mode # a - 辅助模式 f - 全模式 gp-果盘只进入游戏

        V = ['com.supercell.clashofclans.guopan',
             'com.tencent.tmgp.supercell.clashofclans']
        self._app = V[ver]
        
        #-----------------------
        self.COUNT  = dict()
        self.COUNT['EnterGame'] = 0
        self.COUNT['collect'] = 0
        #------------------------

        self.coordinate = []
        self.dWidth, self.dHeight = self.d.window_size() 
        resol = str(self.dWidth) + "x" + str(self.dHeight)
        self.coord = load_configure("Games/Coc.json",resol)

        self.config = load_configure("Games/GameConfig.json","COC")


    def dectect_app(self):
        pid = self.d.app_wait(self._app, front=True) # 等待应用运行, return pid(int)

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
        while True:            
            EXISTS = lambda a,b: self.d(text=a, className=b).exists()
            CLICK = lambda a,b: self.d(text=a, className=b).click()
            try:
                #是否运行游戏 并 存在Textview的文字为进入游戏
                if self.dectect_app() and EXISTS("进入游戏",TEXTVIEW):
                    CLICK("进入游戏",TEXTVIEW)
                    self.COUNT['EnterGame'] += 1 
                    prt("点击进入游戏 次数",COUNT['EnterGame'])
                    ss(1)
                    self._tap(r = True)
                #睡眠100秒
                ss(100)
            except(Exception):
                #睡眠5分钟当有其他操作
                ss(60*5)
        '''
        # 常用写法，注册匿名监控
        self.d.watcher.when("进入游戏").click()
        # 开始后台监控
        self.d.watcher.start(2.0) # 默认监控间隔2.0s
        '''

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
            target = T_Img[a]
            x,y = CV.Match(CHOP(),target)
            if not (x==-1 or y == -1):
                msg("找到",target,"点击",b,",",c) 
                self._tap(x+b,y+c)
                ss(1)

        Words = ['随','谢谢']
        for EW in Words:
            if EW in Text :
                ss(1)
                #检测可捐数值
                #几种捐赠的方案 35 - 气球和雷龙 30 - 雷龙
                for do in D_List:
                    CLICK(do,w,h)
                    #print(target)
                break
        

        #提取所需捐赠兵种
        To_D = list()
        for do in D_List:
            if do in Text:
                To_D.append(do)

        #依次点击要捐赠的兵种
        for do in To_D:
            if do in T_Img:
                CLICK(do,w,h)
                    

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
            ss(1)

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
        if r_color(c,cb, diff = 12):
            #打开聊天框
            x,y = self.coord['Donation']['open']
            self._tap(x,y)
            self.donate2()
            ss(1)
        elif r_color(c,cg, diff = 12):#颜色判断是否在聊天界面
            self.donate2()
            ss(1)
        else:
            msg(c,cb,type(c),type(cb),"未知错误")
            self._tap(555,555,r = True)

    def collect(self):
        ss(1)
        target = self.coord['Collection']
        #print(target)
    
        #找到金币 金水 黑水 
        for tar in target:
            x,y = CV.Match(self._srcv(),tar,d= True,criteria = 0.92)
            if not (x==-1 or y == -1):
                self._tap(x,y)
                self.COUNT['collect'] += 1
                ss(1)
        msg("收集资源 次数:",self.COUNT['collect'])
        ss(1)
        
    def reset_gamescreen(self):
        ss()
        self.d.swipe(280, 120, 1000, 560)
        ss(2)
        try:
            threading.Thread(target= self.Room_in_1 ).start()
            threading.Thread(target= self.Room_in_2 ).start()
        except:
            print ("Error: 线程无法启动线程")
        ss()
        msg("调整游戏视角")

    def Room_in_1(self):
        self.d.touch.down(200, 356) # 模拟按下
        time.sleep(1) # down 和 move 之间的延迟，自己控制
        self.d.touch.move(400, 356) # 模拟移动
        self.d.touch.up(400, 356) # 模拟抬起

    def Room_in_2(self):
        self.d.touch.down(1000, 408) # 模拟按下
        time.sleep(1) # down 和 move 之间的延迟，自己控制
        self.d.touch.move(800, 408) # 模拟移动
        self.d.touch.up(800, 408) # 模拟抬起

    def AddTroops(self):
        pass

    def OutForSleep(self,s = 10):
        HOME = lambda: self.d.press("home")

        HOME()
        msg("返回主界面等待" + str(s) + "分钟后启动游戏")
        ss(60*s)
        self.LaunchCOC()

    def run(self):
        if self._DEBUG:
            self.donate()
            CV.Save(self.d)
            #self.donate3("随意")
            return
        while True:
            try:
                if self._app == 'com.supercell.clashofclans.guopan':
                    self.GPEG()
                #self.reset_gamescreen()

                if self._mode == 'gp':
                    continue

                elif self._mode == 'a':
                    #资源收集
                    self.collect()
                    #捐兵
                    self.donate()
                    #造兵
                    self.AddTroops()

                    self.OutForSleep()

                elif self._mode == 'f':
                    #资源收集
                    self.collect()
                    #造兵检测
                    
                    #捐兵检测
                    self.donate()

                    #出兵检测
                    
                    #升级检测
                    
                    #夜世界
                    
                    #夜世界升级检测
                    
                    #夜世界出兵
            except:
                print ("Error: 线程无法启动线程")

        
                
                

    

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

