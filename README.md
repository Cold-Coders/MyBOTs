# COC-BOT

## Installation

### Windows
- [Python3](https://www.python.org/)
- [Android Studio](https://developer.android.com/studio/#downloads)
- [JDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
- [Appium](https://github.com/appium/appium-desktop/releases/tag/v1.15.1)
- [uiautomator2](https://github.com/openatx/uiautomator2)
- [uiautomatorviewer] ...\Android\Sdk\tools\bin\uiautomatorviewer
```bash
pip install Appium-Python-Client
pip install pytest

# Android System Version
adb shell getprop ro.build.version.release
# Current Android Activity
adb shell "dumpsys window w | grep mCurrent"

# install uiautomator2
pip3 install -U uiautomator2
# 安装包含httprpc服务的apk到手机+atx-agent
# 1.3.0之后的版本，当运行python代码u2.connect()时就会自动推送这些文件了）
python -m uiautomator2 init
```

