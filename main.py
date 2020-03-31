import sys
import uiautomator2 as u2

from GUI.SELECTADEVICE import DEVICE
from GUI.SELECTEMU import EMULATOR
from GUI.SELECTGAME import SELECTGAME


from COC.COC_GUI import COC_BOT_GUI

if __name__ == "__main__":
	config = {}

	config['Win32'] = True if sys.platform == 'win32' else False
	
	# select a device
	DEVICE(config).start()

	# select for correct emulator
	if config['device'] is not None and "emulator" in config['device']:
		EMULATOR(config)

	#select for games
	config['d'] = u2.connect( config['device'] )
	SELECTGAME(config)


	#choose bots
	BotList = {'com.supercell.clashofclans.guopan': 1,
				'com.tencent.tmgp.rxcq': 2,
				'com.supercell.clashofclans': 1
	}

	MyBot = None
	if BotList[ config['game'] ] == 1:
		MyBot = COC_BOT_GUI(config)

	elif BotList[ config['game'] ] == 2:
		pass	

	if MyBot is not None:
		MyBot.start()

