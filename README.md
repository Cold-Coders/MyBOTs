# MyBOTs

## Function
- [x] 

## Installation

### Windows
- [Python3](https://www.python.org/)
- [Android Studio](https://developer.android.com/studio/#downloads)
- [JDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
- [Appium](https://github.com/appium/appium-desktop/releases/tag/v1.15.1)
- [uiautomator2](https://github.com/openatx/uiautomator2)
- [uiautomatorviewer] ...\Android\Sdk\tools\bin\uiautomatorviewer
- [tesseract-v5.0.0](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe)
```bash
pip install Appium-Python-Client
pip install pytest
pip install simplejson

# Android System Version
adb shell getprop ro.build.version.release
# Current Android Activity
adb shell "dumpsys window w | grep mCurrent"

# install uiautomator2
pip3 install -U uiautomator2
# 安装包含httprpc服务的apk到手机+atx-agent
# 1.3.0之后的版本，当运行python代码u2.connect()时就会自动推送这些文件了）
python -m uiautomator2 init
# install weditor
pip install -U weditor
#Windows系统可以使用命令在桌面创建一个快捷方式 weditor --shortcut
#命令行直接输入 weditor 会自动打开浏览器，输入设备的ip或者序列号，点击Connect即可

adb -s emulator-5556 shell rm /data/local/tmp/minicap
adb -s emulator-5556 shell rm /data/local/tmp/minicap.so

pip freeze > requirements.txt

pip list --outdated | grep 'uiautomator2'
pip list --outdated | finstr 'uiautomator2'


## VirtualEnvironment
python3 -m venv bots
. bots/bin/activate
pip install -r requirements.txt
```

