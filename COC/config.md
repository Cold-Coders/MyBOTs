# Config
- self.config - type(dict) configure of Bot 				
	- .config['lang'] - language of GUI
- self.lang   - type(dict) configure of language
- self.em 	- type(int) Emulator's pid
- self.d 		
	- type(str) Device's name before connect
	- type(obj) Device's automator engine after connected
- self.func   
	- type(List) Functionality of the bots 
- self.lang['func_name'] - type(List) name of Function #在语言配置里增加减少修改
	0. - 自动捐赠
	1. - 自动降杯
	2. - 自动打鱼

- self.lang['test_name'] - type(List) name of Function #在语言配置里
- self.test_button	   - type(List) button of test function
	0. - 缩放
	1. - 收集资源
	2. - 捐兵测试

- self.lang['info_name'] - type(List) name of Information board
	0. - "金钱"
	1. - "红水"
	2. - "黑水"
	3. - "累计掠夺金币"
	4. - "累计掠夺红水"
	5. - "累计掠夺黑水"
