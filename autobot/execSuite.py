__author__="JG"
##-----DO NOT MAKE ANY CHANGES TO THIS FILE-----#


from autobot.lib import utility as util
import unittest
import HtmlTestRunner
import logging
import time
import sys
import os
from datetime import datetime
from autobot.testcases import test00_ping_pong_life_cycle

logging.basicConfig(filename='execTraces.log', format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(test00_ping_pong_life_cycle.PingPongLifeCycle))
report = 'execReport.html'
with open(report, "w") as buff:
    runner = HtmlTestRunner.HTMLTestRunner(stream=buff)
    result = runner.run(suite)


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='reports', report_name='execReport.html'))

