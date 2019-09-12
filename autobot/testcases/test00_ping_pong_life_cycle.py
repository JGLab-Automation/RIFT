__author__ = "JG"

import unittest
from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.config import constants as const
import sys

class PingPongLifeCycle(unittest.TestCase):

    const.proj_name = "test00"
    const.proj_desc = "test00_ping_pong_life_cycle"
    nsr_id = ""

    def test01_Project_Add(self):
        util.log_info(f"Executing {self.test01_Project_Add.__name__}.")

        fw.proj_add(const.lp_addr, const.header, const.proj_name, const.proj_desc)

        name = fw.get_proj_name(const.lp_addr, const.header, const.proj_name)
        if name == const.proj_name:
            util.log_info(f"Project- {name}, added successfully. Test-case Pass.")
        else:
            assert name == const.proj_name, f"Expected- {const.proj_name}, Configured- {name}. Test-case Fail."

    def test02_Project_Configure(self):
        util.log_info(f"Executing {self.test02_Project_Configure.__name__}.")

        fw.proj_config(const.lp_addr, const.header, const.proj_name, const.proj_user_name,
                       const.proj_user_domain, const.proj_role, const.proj_event_publish)

        config = fw.get_proj_user_role(const.lp_addr, const.header, const.proj_name)
        if config["role"] == "rw-project:project-admin":
            util.log_info(f"Project- {const.proj_name} configured with user-role- {config['role']}. Test-case Pass.")
        else:
            assert config["role"] == "rw-project:project-admin", \
                f"Expected- rw-project:project-admin, Configured- {config['role']}. Test-case Fail."

    def test03_Cloud_Account_Add(self):
        util.log_info(f"Executing {self.test03_Cloud_Account_Add.__name__}.")

        fw.cloud_acct_add(const.lp_addr, const.header, const.proj_name, const.cloud_acct_name,
                          const.cloud_acct_type, const.cloud_acct_timeout)
        acct_type = fw.get_cloud_acct_type(const.lp_addr, const.header, const.proj_name, const.cloud_acct_name)
        if acct_type == "openstack":
            util.log_info(f"Account- {const.cloud_acct_name} added for account-type {acct_type}. Test-case Pass.")
        else:
            assert acct_type == "openstack", f"Expected- openstack, Configured- {acct_type}. Test-case Fail."

    def test04_Cloud_Account_Configure(self):
        util.log_info(f"Executing {self.test04_Cloud_Account_Configure.__name__}.")

        fw.cloud_acct_config_openstack(const.lp_addr, const.header, const.proj_name, const.cloud_acct_name,
                                       const.vim_os_key, const.vim_os_secret, const.vim_os_auth_url, const.vim_os_tenant
                                       )
        status = fw.cloud_acct_status(const.lp_addr, const.header, const.proj_name, const.cloud_acct_name)
        if status == "success":
            util.log_info(f"Cloud-account {const.cloud_acct_name} added successfully. Test-case Pass.")
        else:
            assert status == "success", f"Expected- success, Configured- {status}. Test-case Fail."

    def test05_Package_Onboard(self):
        util.log_info(f"Executing {self.test05_Package_Onboard.__name__}.")

        transac_id = fw.pkg_onboard(const.lp_addr, const.header, const.proj_name, const.ping_vnfd_ext_url)
        state1 = fw.pkg_upload_status(const.lp_addr, const.header, const.proj_name, transac_id)
        transac_id = fw.pkg_onboard(const.lp_addr, const.header, const.proj_name, const.pong_vnfd_ext_url)
        state2 = fw.pkg_upload_status(const.lp_addr, const.header, const.proj_name, transac_id)
        transac_id = fw.pkg_onboard(const.lp_addr, const.header, const.proj_name, const.ping_pong_nsd_ext_url)
        state3 = fw.pkg_upload_status(const.lp_addr, const.header, const.proj_name, transac_id)

        if state1 and state2 and state3 == "COMPLETED":
            util.log_info(f"Ping VNFD, Pong VNFD & Ping_Pong NSD are uploaded in project- {const.proj_name}. "
                          f"Test-case Pass.")
        else:
            assert state1 and state2 and state3 == "COMPLETED", f"Expected- COMPLETED, Received- {state1, state2, state3}. " \
                f"Test-case Fail."

    def test06_NS_Create(self):
        util.log_info(f"Executing {self.test06_NS_Create.__name__}.")

        ns_name = "AutoTest"
        nsd = fw.get_nsd_name_id(const.lp_addr, const.header, const.proj_name)
        nsd_id = nsd["ping_pong_nsd"]
        nsr_id = fw.ns_create(const.lp_addr, const.header, const.proj_name, ns_name, nsd_id)
        self.nsr_id = nsr_id

        conf_name = fw.get_ns_instance_config(const.lp_addr, const.header, const.proj_name, self.nsr_id, "name")
        conf_state = fw.get_ns_instance_config(const.lp_addr, const.header, const.proj_name, self.nsr_id, "status")

        if conf_name == ns_name and conf_state == "DISABLED":
            util.log_info(f"NS is created with name- {conf_name} and current state is- {conf_state}. Test-case Pass.")
        else:
            assert conf_name == ns_name and conf_state == "DISABLED", \
                f"Expected name- {ns_name}, Configured name- {conf_name}. Test-case Fail."

    def test07_NS_Instantiate(self):
        util.log_info(f"Executing {self.test07_NS_Instantiate.__name__}.")

        fw.ns_instantiate(const.lp_addr, const.header, const.proj_name, self.nsr_id)
        conf_state = fw.get_ns_instance_config(const.lp_addr, const.header, const.proj_name, self.nsr_id, "status")
        state = fw.get_ns_oper_status(const.lp_addr, const.header, const.proj_name, self.nsr_id)
        if conf_state == "ENABLED" and state == "running":
            util.log_info(f"NS with ID- {self.nsr_id} instantiated successfully and is- {state}. Test-case Pass.")
        else:
            assert conf_state == "ENABLED" and state == "running", \
                f"Expected state- running, Current state- {state}. Test-case Fail."

    def test08_NS_Terminate(self):
        util.log_info(f"Executing {self.test08_NS_Terminate.__name__}.")

        state = fw.get_ns_oper_status(const.lp_addr, const.header, const.proj_name, self.nsr_id)
        if state == "running":
            fw.ns_terminate(const.lp_addr, const.header, const.proj_name, self.nsr_id)
            conf_state = fw.get_ns_instance_config(const.lp_addr, const.header, const.proj_name, self.nsr_id, "status")
            state = fw.get_ns_oper_status(const.lp_addr, const.header, const.proj_name, self.nsr_id)
            if conf_state == "DISABLED" and state == "terminated":
                util.log_info(f"NS with NSR ID- {self.nsr_id} terminated successfully. Test-case Pass.")
            else:
                assert conf_state == "DISABLED" and state == "terminated", \
                    f"Expected state- terminated, Current state- {state}. Test-case Fail."
        else:
            assert state == "running", f"NS with NSR ID- {self.nsr_id} is not running. Current state- {state}. " \
                f"Test-case Fail."

    def test09_NS_Delete(self):
        util.log_info(f"Executing {self.test09_NS_Delete.__name__}.")

        conf_state = fw.get_ns_instance_config(const.lp_addr, const.header, const.proj_name, self.nsr_id, "status")
        state = fw.get_ns_oper_status(const.lp_addr, const.header, const.proj_name, self.nsr_id)
        if conf_state == "DISABLED" or state == "terminated":
            fw.ns_delete(const.lp_addr, const.header, const.proj_name, self.nsr_id)
            conf_state = fw.get_ns_instance_config(const.lp_addr, const.header, const.proj_name, self.nsr_id)
            if not conf_state:
                util.log_info(f"NS with NSR ID- {self.nsr_id} deleted successfully. Test-case Pass.")
            else:
                util.log_info(f"NS with NSR ID- {self.nsr_id} is not deleted. NS still has config-data- {conf_state}."
                              f"Test-case Fail.")
        else:
            assert conf_state == "DISABLED" or state == "terminated",\
                f"NS with NSR ID- {self.nsr_id} is not terminated. Current state- {state}. Test-case Fail."

    def test10_Package_Delete(self):
        vnfd_id = fw.get_vnfd_id(const.lp_addr, const.header, const.proj_name)
        state1 = fw.pkg_delete(const.lp_addr, const.header, const.proj_name, "nsd", "ping_pong_nsd")
        state2 = fw.pkg_delete(const.lp_addr, const.header, const.proj_name, "vnfd", "pong_vnfd")
        state3 = fw.pkg_delete(const.lp_addr, const.header, const.proj_name, "vnfd", "ping_vnfd")

        if state1 and state2 and state3 == "OK":
            util.log_info("Packages deleted successfully.")
            util.log_info(f"Test-case: {self.test10_Package_Delete.__name__} | Status: Passed.")
        else:
            assert state1 and state2 and state3 == "OK", f"Response States: {state1, state2, state3}." \
                f"Status: Failed."

    def test11_Cloud_Account_Delete(self):
        util.log_info(f"Executing {self.test11_Cloud_Account_Delete.__name__}.")
        state = fw.cloud_acct_delete(const.lp_addr, const.header, const.proj_name, const.cloud_acct_name)
        if state == "OK":
            util.log_info(f"Test-case: {self.test11_Cloud_Account_Delete.__name__} | Status: Passed.")
        else:
            assert state == "OK", f"Response State: {state}. Status: Failed."

    def test12_Project_Delete(self):
        util.log_info(f"Executing {self.test12_Project_Delete.__name__}.")
        state = fw.proj_delete(const.lp_addr, const.header, const.proj_name)
        if state == "OK":
            util.log_info(f"Test-case: {self.test12_Project_Delete.__name__} | Status: Passed.")
        else:
            assert state == "OK", f"Response State: {state}. Status: Failed."


#
# if __name__ == '__main__':
#     unittest.main()
