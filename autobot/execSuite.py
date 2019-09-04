__author__="JG"
##-----DO NOT MAKE ANY CHANGES TO THIS FILE-----#


from autobot.lib import utility as util
import HtmlTestRunner
import unittest
import logging
import time
import sys
import os
from datetime import datetime


##-----Generating suite execution logs-----#
logging.basicConfig(filename='execTraces.log', format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
now = str(datetime.now()).replace(' ', '_')


InitialNotification="FMPS Regression-suite execution is initiating now."
util.send_email(InitialNotification, "Joyanto.Ghosh@FireEye.com", "Joyanto.Ghosh@FireEye.com", "Notice: FMPS Regression-suite execution is initiating now.", cc="", attachment="")


##-----Creating Test suite-----#
suite = unittest.TestSuite()
suite.addTests(unittest.load_tests())
suite.addTest(unittest.makeSuite(TestCases.FileType_Analysis))
suite.addTest(unittest.makeSuite(TestCases.Parallel_Scan))

dateTimeStamp = time.strftime('%Y%m%d_%H_%M_%S')


report_file = 'execReport.html'
with open(report_file, 'w') as file:
    runner = HtmlTestRunner.HTMLTestRunner(stream=file, report_title="Test suite report.", descriptions="")
result = runner.run(suite)



FinalReport = open(report_file, "r")
EmailMessage = FinalReport.read()
FinalReport.close()

##-----Sending email report-----#
util.log_info("> Sending email to the recipients.\n")
util.send_email(EmailMessage, "Joyanto.Ghosh@FireEye.com", "Sunil.Chacko@FireEye.com, Joyanto.Ghosh@FireEye.com", "Result: FMPS Regression-suite Execution on v%s (%s)." % (str(BuildID), str(TestCases.TestExecutionBuild[0])), cc="", attachment=report_file)
util.log_info("-"*100)
buf.close()
sys.exit(TestResult.failure_count + TestResult.error_count)

##-----End of Execution File-----#