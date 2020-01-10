import unittest
import uiautomator2 as u2
import sys
sys.path.append("..")
from util import *
#from appium import webdriver

class GP_COC:
    def __init__(self):
        self._DEBUG = False
        self.d = u2.connect("emulator-5554")
        self.dWidth, self.dHeight = self.d.window_size()
        self._app = 'com.supercell.clashofclans.guopan'
        self._mode = 'a' # a - 辅助模式 b - 执行模式

    def dectect_app(self):
        pid = self.d.app_wait(self._app) # 等待应用运行, return pid(int)

        if self._DEBUG:
            if not pid:
                print(self._app,"is not running")
            else:
                print(self._app,"pid is %d" % pid)

        return pid

    def assist(self):
        COUNT  = dict()

        TEXTVIEW = lambda: 'android.widget.TextView'
        EXISTS = lambda a,b: self.d(text=a, className=b).exists()
        CLICK = lambda a,b: self.d(text=a, className=b).click()
        try:
            #是否运行游戏 并 存在Textview的文字为进入游戏
            if self.dectect_app and EXISTS("进入游戏",TEXTVIEW):
                CLICK("进入游戏",TEXTVIEW)
                COUNT[EnterGame] += 1 
                prt("点击进入游戏次数",COUNT[EnterGame])
            #睡眠100秒
            ss(100)
        except(Exception):
            #睡眠5分钟当有其他操作
            ss(60*5)


    def run(self):
        while True:
            if self._mode == 'a':
                self.assist()


                

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

