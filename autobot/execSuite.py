__author__="JG"



from autobot.lib import utility as util
import unittest
import HtmlTestRunner
import logging
import time
import sys
import os
from datetime import datetime
from autobot.testcases import test00_ping_pong_life_cycle as tc1


logging.basicConfig(filename='traces/execTraces.log', format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(tc1.PingPongLifeCycle))

runner = HtmlTestRunner.HTMLTestRunner(report_name='execReport', report_title="Regression Suite Execution")
result = runner.run(suite)
unittest.main(testRunner=runner)
#runner.generateReport(None, result)

# report = "execReport.html"
# with open(report, "w") as buf:
#     runner = HtmlTestRunner.HTMLTestRunner(report_name='execReport: ', report_title="Exec Report", stream=buf)
#     result = runner.run(suite)
#     unittest.main(testRunner=runner)
#     runner.generateReport(None, result)

