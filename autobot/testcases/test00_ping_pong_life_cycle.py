__author__ = "JG"

import unittest
from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.config import constants as const


class PingPongLifeCycle(unittest.TestCase):

    proj_name = ["test00"]
    proj_desc = "test00_ping_pong_life_cycle"
    nsr_id = []

    def test01_Project_Add(self):
        util.log_info(f"Executing {self.test01_Project_Add.__name__}.")

        fw.proj_add(const.lp_addr_default[0], const.header_default, self.proj_name[0], self.proj_desc)

        name = fw.get_proj_name(const.lp_addr_default[0], const.header_default, self.proj_name[0])
        if name == self.proj_name[0]:
            util.log_info(f"Project- {name}, added successfully. Test-case Pass.")
        else:
            util.log_info(f"Expected- {self.proj_name[0]}, Configured- {name}. Test-case Fail.")
            assert name == self.proj_name[0], f"Expected- {self.proj_name[0]}, Configured- {name}. Test-case Fail."

    def test02_Project_Configure(self):
        util.log_info(f"Executing {self.test02_Project_Configure.__name__}.")

        fw.proj_config(const.lp_addr_default[0], const.header_default, self.proj_name[0], const.proj_user_name,
                       const.proj_user_domain, const.proj_role, const.proj_event_publish)

        config = fw.get_proj_user_role(const.lp_addr_default[0], const.header_default, self.proj_name[0])
        if config["role"] == "rw-project:project-admin":
            util.log_info(f"Project- {self.proj_name[0]} configured with user-role- {config['role']}. Test-case Pass.")
        else:
            util.log_info(f"Expected- rw-project:project-admin, Configured- {config['role']}. Test-case Fail.")
            assert config["role"] == "rw-project:project-admin", \
                f"Expected- rw-project:project-admin, Configured- {config['role']}. Test-case Fail."

    def test03_Cloud_Account_Add(self):
        util.log_info(f"Executing {self.test03_Cloud_Account_Add.__name__}.")

        fw.cloud_acct_add(const.lp_addr_default[0], const.header_default, self.proj_name[0], const.cloud_acct_name[0],
                          const.cloud_acct_type[0], const.cloud_acct_timeout[0])
        acct_type = fw.get_cloud_acct_type(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                           const.cloud_acct_name[0])
        if acct_type == "openstack":
            util.log_info(f"Account- {const.cloud_acct_name[0]} added for account-type {acct_type}. Test-case Pass.")
        else:
            util.log_info(f"Expected- openstack, Configured- {acct_type}. Test-case Fail.")
            assert acct_type == "openstack", f"Expected- openstack, Configured- {acct_type}. Test-case Fail."

    def test04_Cloud_Account_Configure(self):
        util.log_info(f"Executing {self.test04_Cloud_Account_Configure.__name__}.")

        fw.cloud_acct_config_openstack(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                       const.cloud_acct_name[0], const.vim_os_key, const.vim_os_secret,
                                       const.vim_os_auth_url, const.vim_os_tenant)
        status = fw.cloud_acct_status(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                      const.cloud_acct_name[0])
        if status == "success":
            util.log_info(f"Cloud-account {const.cloud_acct_name[0]} added successfully. Test-case Pass.")
        else:
            util.log_info(f"Expected- success, Configured- {status}. Test-case Fail.")
            assert status == "success", f"Expected- success, Configured- {status}. Test-case Fail."

    def test05_Package_Onboard(self):
        util.log_info(f"Executing {self.test05_Package_Onboard.__name__}.")

        transac_id = fw.pkg_onboard(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                    const.ping_vnfd_ext_url)
        state1 = fw.pkg_upload_status(const.lp_addr_default[0], const.header_default, self.proj_name[0], transac_id)
        transac_id = fw.pkg_onboard(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                    const.pong_vnfd_ext_url)
        state2 = fw.pkg_upload_status(const.lp_addr_default[0], const.header_default, self.proj_name[0], transac_id)
        transac_id = fw.pkg_onboard(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                    const.ping_pong_nsd_ext_url)
        state3 = fw.pkg_upload_status(const.lp_addr_default[0], const.header_default, self.proj_name[0], transac_id)

        if state1 and state2 and state3 == "COMPLETED":
            util.log_info(f"Ping VNFD, Pong VNFD & Ping_Pong NSD are uploaded in project- {self.proj_name[0]}. "
                          f"Test-case Pass.")
        else:
            util.log_info(f"Expected- COMPLETED, Received- {state1, state2, state3}. Test-case Fail.")
            assert state1 and state2 and state3 == "COMPLETED", \
                f"Expected- COMPLETED, Received- {state1, state2, state3}. Test-case Fail."

    def test06_NS_Create(self):
        util.log_info(f"Executing {self.test06_NS_Create.__name__}.")

        ns_name = "AutoTest"
        nsd = fw.get_nsd_name_id(const.lp_addr_default[0], const.header_default, self.proj_name[0])
        nsd_id = nsd["ping_pong_nsd"]
        nsr_id = fw.ns_create(const.lp_addr_default[0], const.header_default, self.proj_name[0], ns_name, nsd_id)
        self.nsr_id.append(nsr_id)

        conf_name = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                              self.nsr_id[0], "name")
        conf_state = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                               self.nsr_id[0], "status")

        if conf_name == ns_name and conf_state == "DISABLED":
            util.log_info(f"NS is created with name- {conf_name} and current state is- {conf_state}. Test-case Pass.")
        else:
            util.log_info(f"Expected name- {ns_name}, Configured name- {conf_name}. Test-case Fail.")
            assert conf_name == ns_name and conf_state == "DISABLED", \
                f"Expected name- {ns_name}, Configured name- {conf_name}. Test-case Fail."

    def test07_NS_Instantiate(self):
        util.log_info(f"Executing {self.test07_NS_Instantiate.__name__}.")

        fw.ns_instantiate(const.lp_addr_default[0], const.header_default, self.proj_name[0], self.nsr_id[0])
        conf_state = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                               self.nsr_id[0], "status")
        state = fw.get_ns_oper_status(const.lp_addr_default[0], const.header_default, self.proj_name[0], self.nsr_id[0])
        if conf_state == "ENABLED" and state == "running":
            util.log_info(f"NS with ID- {self.nsr_id[0]} instantiated successfully and is- {state}. Test-case Pass.")
        else:
            util.log_info(f"Expected state- running, Current state- {state}. Test-case Fail.")
            assert conf_state == "ENABLED" and state == "running", \
                f"Expected state- running, Current state- {state}. Test-case Fail."

    def test08_NS_Terminate(self):
        util.log_info(f"Executing {self.test08_NS_Terminate.__name__}.")

        state = fw.get_ns_oper_status(const.lp_addr_default[0], const.header_default, self.proj_name[0], self.nsr_id[0])
        if state == "running":
            fw.ns_terminate(const.lp_addr_default[0], const.header_default, self.proj_name[0], self.nsr_id[0])
            conf_state = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                                   self.nsr_id[0], "status")
            state = fw.get_ns_oper_status(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                          self.nsr_id[0])
            if conf_state == "DISABLED" and state == "terminated":
                util.log_info(f"NS with NSR ID- {self.nsr_id[0]} terminated successfully. Test-case Pass.")
            else:
                util.log_info(f"Expected state- terminated, Current state- {state}. Test-case Fail.")
                assert conf_state == "DISABLED" and state == "terminated", \
                    f"Expected state- terminated, Current state- {state}. Test-case Fail."
        else:
            util.log_info(f"NS with NSR ID- {self.nsr_id[0]} is not running. Current state- {state}. Test-case Fail.")
            assert state == "running", f"NS with NSR ID- {self.nsr_id[0]} is not running. " \
                f"Current state- {state}. Test-case Fail."

    def test09_NS_Delete(self):
        util.log_info(f"Executing {self.test09_NS_Delete.__name__}.")

        conf_state = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                               self.nsr_id[0], "status")
        state = fw.get_ns_oper_status(const.lp_addr_default[0], const.header_default, self.proj_name[0], self.nsr_id[0])
        if conf_state == "DISABLED" or state == "terminated":
            fw.ns_delete(const.lp_addr_default[0], const.header_default, self.proj_name[0], self.nsr_id[0])
            conf_state = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                                   self.nsr_id[0])
            if not conf_state:
                util.log_info(f"NS with NSR ID- {self.nsr_id[0]} deleted successfully. Test-case Pass.")
            else:
                util.log_info(f"NS with NSR ID- {self.nsr_id[0]} is not deleted. "
                              f"NS still has config-data- {conf_state}. Test-case Fail.")
                assert not conf_state, f"NS with NSR ID- {self.nsr_id[0]} is not deleted. " \
                    f"NS still has config-data- {conf_state}. Test-case Fail."
        else:
            util.log_info(f"NS with NSR ID- {self.nsr_id[0]} is not terminated. Current state- {state}. "
                          f"Test-case Fail.")
            assert conf_state == "DISABLED" or state == "terminated",\
                f"NS with NSR ID- {self.nsr_id[0]} is not terminated. Current state- {state}. Test-case Fail."

    def test10_Package_Delete(self):
        util.log_info(f"Executing {self.test10_Package_Delete.__name__}.")

        pkg_catalog = fw.get_pkg_catalog(const.lp_addr_default[0], const.header_default, self.proj_name[0])
        if pkg_catalog:
            fw.pkg_delete(const.lp_addr_default[0], const.header_default, self.proj_name[0], "nsd", "ping_pong_nsd")
            fw.pkg_delete(const.lp_addr_default[0], const.header_default, self.proj_name[0], "vnfd", "pong_vnfd")
            fw.pkg_delete(const.lp_addr_default[0], const.header_default, self.proj_name[0], "vnfd", "ping_vnfd")

            pkg_catalog = fw.get_pkg_catalog(const.lp_addr_default[0], const.header_default, self.proj_name[0])
            if pkg_catalog is None:
                util.log_info("Packages deleted successfully. Test-case Pass.")
            else:
                util.log_info("Packages couldn't delete successfully. Test-case Fail.")
                assert pkg_catalog is None, "Packages couldn't delete successfully. Test-case Fail."
        else:
            util.log_info(f"Packages not available to delete. Test-case Fail.")
            assert pkg_catalog, f"Packages not available to delete. Test-case Fail."

    def test11_Cloud_Account_Delete(self):
        util.log_info(f"Executing {self.test11_Cloud_Account_Delete.__name__}.")

        acct = fw.get_cloud_acct_details(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                         const.cloud_acct_name[0])
        if acct:
            fw.cloud_acct_delete(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                 const.cloud_acct_name[0])
            acct = fw.get_cloud_acct_details(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                             const.cloud_acct_name[0])
            if not acct:
                util.log_info(f"Cloud account with name- {const.cloud_acct_name[0]} deleted successfully. "
                              f"Test-case Pass.")
            else:
                util.log_info(f"Cloud account with name- {const.cloud_acct_name[0]} couldn't get deleted. "
                              f"Test-case Fail.")
                assert not acct, f"Cloud account with name- {const.cloud_acct_name[0]} couldn't get deleted. " \
                    f"Test-case Fail."
        else:
            util.log_info(f"Cloud account with name- {const.cloud_acct_name[0]} is not configured. Test-case Fail.")
            assert acct, f"Cloud account with name- {const.cloud_acct_name[0]} is not configured. Test-case Fail."

    def test12_Project_Delete(self):
        util.log_info(f"Executing {self.test12_Project_Delete.__name__}.")

        proj_details = fw.get_proj_details(const.lp_addr_default[0], const.header_default, self.proj_name[0])
        if proj_details:
            fw.proj_delete(const.lp_addr_default[0], const.header_default, self.proj_name[0])
            proj_details = fw.get_proj_details(const.lp_addr_default[0], const.header_default, self.proj_name[0])
            if proj_details is None:
                util.log_info(f"Project with name- {self.proj_name[0]} deleted successfully. Test-case Pass.")
            else:
                util.log_info(f"Expected- None, Actual- {proj_details}. Test-case Fail.")
                assert proj_details is None, f"Expected- None, Actual- {proj_details}. Test-case Fail."
        else:
            util.log_info(f"Project details not found to delete. Test-case Fail.")
            assert proj_details, f"Project details not found to delete. Test-case Fail."


if __name__ == '__main__':
    unittest.main()
