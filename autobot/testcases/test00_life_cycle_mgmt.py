__author__ = "JG"

import unittest
from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.config import constants as const


class Life_Cycle_Management(unittest.TestCase):

    def test01_Project_Add(self):
        state = fw.proj_add(const.lp_addr, const.header, const.proj_name_default, const.proj_desc_default)
        if state == "OK":
            util.log_info(f"Test-case: {self.test01_Project_Add.__name__} | Status: Passed.")
        else:
            assert state == "OK", f"Response State: {state}. Status: Failed."

    def test02_Project_Configure(self):
        state = fw.proj_config(const.lp_addr, const.header, const.proj_name_default, const.proj_user_name,
                               const.proj_user_domain, const.proj_role, const.proj_event_publish)
        if state == "OK":
            util.log_info(f"Test-case: {self.test02_Project_Configure.__name__} | Status: Passed.")
        else:
            assert state == "OK", f"Response State: {state}. Status: Failed."

    def test03_Cloud_Account_Add(self):
        state = fw.cloud_acct_add(const.lp_addr, const.header, const.proj_name_default, const.cloud_acct_name,
                                  const.cloud_acct_type, const.cloud_acct_timeout)
        if state == "OK":
            util.log_info(f"Test-case: {self.test03_Cloud_Account_Add.__name__} | Status: Passed.")
        else:
            assert state == "OK", f"Response State: {state}. Status: Failed."

    def test04_Cloud_Account_Configure(self):
        state = fw.cloud_acct_config_openstack(const.lp_addr, const.header, const.proj_name_default,
                                                const.cloud_acct_name, const.vim_os_key, const.vim_os_secret,
                                               const.vim_os_auth_url, const.vim_os_tenant)
        if state == "OK":
            status = fw.cloud_acct_status(const.lp_addr, const.header, const.proj_name, const.cloud_acct_name)
            if status == "success":
                util.log_info(f"Test-case: {self.test04_Cloud_Account_Configure.__name__} | Status: Passed.")
            else:
                assert state == "OK", f"Response State: {state}. Status: Failed."
        else:
            assert state == "OK", f"Response State: {state}. Status: Failed."

    def test05_Descriptors_Create(self):
        pass

    def test06_Descriptors_Onboard(self):
        pass

    def test07_NS_Instantiate(self):
        pass

    def test08_NS_Terminate(self):
        pass

    def test09_NS_Delete(self):
        pass

    def test10_Cloud_Account_Delete(self):
        pass

    def test11_Project_Delete(self):
        pass

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()