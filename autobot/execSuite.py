__author__="JG"

from autobot.lib import utility as util
import unittest
import HtmlTestRunner
import logging
import time
import sys
import os
from datetime import datetime
from autobot.testcases import test00_ping_pong_life_cycle as tc0
from autobot.testcases import test01_resource_discovery_openstack as tc1


logging.basicConfig(filename='artifacts/traces/exec.log', format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(tc0.PingPongLifeCycle))
suite.addTest(unittest.makeSuite(tc1.ResourceDiscovery_OpenStack))

runner = HtmlTestRunner.HTMLTestRunner(report_name='execReport', report_title="Regression Suite Execution")
result = runner.run(suite)
unittest.main(testRunner=runner)
runner.generateReport(None, result)


