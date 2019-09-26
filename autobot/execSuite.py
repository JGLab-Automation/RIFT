__author__ = "JG"

import unittest
import HtmlTestRunner
import logging
import time
import sys
import os
from datetime import datetime
from autobot.lib import utility as util
from autobot.lib import framework as fw
from autobot.config import constants as const
from autobot.testcases import test00_ping_pong_life_cycle as tc0
from autobot.testcases import test01_resource_discovery_openstack as tc1
from autobot.testcases import test02_vnf_adoption_openstack as tc2


logging.basicConfig(filename='artifacts/traces/exec.log', format='%(asctime)s:%(levelname)s:%(message)s',
                    level=logging.INFO)
curr_dir = os.path.dirname(os.path.realpath(__file__))
# curr_dir = os.path.dirname(__file__)
const.running_dir.append(curr_dir)

lp_version = fw.get_lp_version(const.lp_addr_default[0], const.header_default)
util.log_info(f"LP under-test is running on v{lp_version}.")

#----- Packaging test-cases in Unittest.
suite = unittest.TestSuite()
# suite.addTest(unittest.makeSuite(tc0.PingPongLifeCycle))
# suite.addTest(unittest.makeSuite(tc1.ResourceDiscoveryOpenStack))
suite.addTest(unittest.makeSuite(tc2.VNFAdoptionOpenStack))

#----- Running test-cases.
description = ""
runner = HtmlTestRunner.HTMLTestRunner(report_name='execReport', report_title=f"Regression Report on v{lp_version}.")
result = runner.run(suite)
# unittest.main(testRunner=runner)
# runner.generateReport(None, result)

#----- Collaborating Reports -----
report_dir = os.path.join(curr_dir, "reports")
fo = open("execReport.html", "w+")

for r, d, f in os.walk(report_dir):
    for reports in f:
        with open(f"{report_dir}/{reports}", "r+") as report:
            for lines in report.readlines():
                fo.write(lines)
fo.close()

#----- Generating System Logs -----
fw.generate_system_log(const.lp_addr_default[0], const.header_default)
fw.download_system_log(const.lp_addr_default[0], const.header_default)

unittest.main(testRunner=runner)

if __name__ == '__main__':
    unittest.main()
    unittest.main(testRunner=runner)
