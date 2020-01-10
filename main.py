import os
import time
from HtmlTestRunner import HTMLTestRunner
import unittest
from Games.GPCOC import GP_COC

DEBUG = False

test_dir = './Games'
discover = unittest.defaultTestLoader.discover(start_dir=test_dir, pattern="*.py")

if __name__ == "__main__":
	if DEBUG:
		HTMLTestRunner(combine_reports=True, report_name="test_report", add_timestamp=False).run(discover)
	else:
		app = GP_COC()
		app.run()
