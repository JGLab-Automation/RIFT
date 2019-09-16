__author__ = "JG"

import unittest
from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.config import constants as const


class ResourceDiscovery_OpenStack(unittest.TestCase):

    proj_name = "test01"
    proj_desc = "test01_resource_discovery_openstack"

    def test01_Project_Add(self):
        util.log_info(f"Executing {self.test01_Project_Add.__name__}.")

        fw.proj_add(const.lp_addr, const.header, self.proj_name, self.proj_desc)

        name = fw.get_proj_name(const.lp_addr, const.header, self.proj_name)
        if name == self.proj_name:
            util.log_info(f"Project- {name}, added successfully. Test-case Pass.")
        else:
            assert name == self.proj_name, f"Expected- {self.proj_name}, Configured- {name}. Test-case Fail."

    def test02_Project_Configure(self):
        util.log_info(f"Executing {self.test02_Project_Configure.__name__}.")

        fw.proj_config(const.lp_addr, const.header, self.proj_name, const.proj_user_name,
                       const.proj_user_domain, const.proj_role, const.proj_event_publish)

        config = fw.get_proj_user_role(const.lp_addr, const.header, self.proj_name)
        if config["role"] == "rw-project:project-admin":
            util.log_info(f"Project- {self.proj_name} configured with user-role- {config['role']}. Test-case Pass.")
        else:
            assert config["role"] == "rw-project:project-admin", \
                f"Expected- rw-project:project-admin, Configured- {config['role']}. Test-case Fail."

    def test03_Cloud_Account_Add(self):
        util.log_info(f"Executing {self.test03_Cloud_Account_Add.__name__}.")

        fw.cloud_acct_add(const.lp_addr, const.header, self.proj_name, const.cloud_acct_name,
                          const.cloud_acct_type, const.cloud_acct_timeout)
        acct_type = fw.get_cloud_acct_type(const.lp_addr, const.header, self.proj_name, const.cloud_acct_name)
        if acct_type == "openstack":
            util.log_info(f"Account- {const.cloud_acct_name} added for account-type {acct_type}. Test-case Pass.")
        else:
            assert acct_type == "openstack", f"Expected- openstack, Configured- {acct_type}. Test-case Fail."

    def test04_Cloud_Account_Configure(self):
        util.log_info(f"Executing {self.test04_Cloud_Account_Configure.__name__}.")

        fw.cloud_acct_config_openstack(const.lp_addr, const.header, self.proj_name, const.cloud_acct_name,
                                       const.vim_os_key, const.vim_os_secret, const.vim_os_auth_url, const.vim_os_tenant
                                       )
        status = fw.cloud_acct_status(const.lp_addr, const.header, self.proj_name, const.cloud_acct_name)
        if status == "success":
            util.log_info(f"Cloud-account {const.cloud_acct_name} added successfully. Test-case Pass.")
        else:
            assert status == "success", f"Expected- success, Configured- {status}. Test-case Fail."

    def test05_Discover_Resource(self):
        util.log_info(f"Executing {self.test05_Discover_Resource.__name__}.")

        fw.vim_resource_discover(const.lp_addr, const.header, self.proj_name, const.cloud_acct_name)
        status = fw.vim_discover_status(const.lp_addr, const.header, self.proj_name, const.cloud_acct_name)
        if status == "discovered":
            util.log_info(f"Resource discovery on account-name- {const.cloud_acct_name} is successful. Test-case Pass.")
        else:
            assert status == "discovered", f"Expected- success, Configured- {status}. Test-case Fail."

    def test06_Cloud_Account_Delete(self):
        util.log_info(f"Executing {self.test06_Cloud_Account_Delete.__name__}.")

        acct = fw.get_cloud_acct_details(const.lp_addr, const.header, self.proj_name, const.cloud_acct_name)
        if acct:
            fw.cloud_acct_delete(const.lp_addr, const.header, self.proj_name, const.cloud_acct_name)
            acct = fw.get_cloud_acct_details(const.lp_addr, const.header, self.proj_name, const.cloud_acct_name)
            if not acct:
                util.log_info(f"Cloud account with name- {const.cloud_acct_name} deleted successfully. Test-case Pass.")
            else:
                assert not acct, f"Cloud account with name- {const.cloud_acct_name} couldn't get deleted." \
                    f"Test-case Fail."
        else:
            assert acct, f"Cloud account with name- {const.cloud_acct_name} is not configured. Test-case Fail."

    def test07_Project_Delete(self):
        util.log_info(f"Executing {self.test07_Project_Delete.__name__}.")

        proj_details = fw.get_proj_details(const.lp_addr, const.header, self.proj_name)
        if proj_details:
            fw.proj_delete(const.lp_addr, const.header, self.proj_name)
            proj_details = fw.get_proj_details(const.lp_addr, const.header, self.proj_name)
            if proj_details is None:
                util.log_info(f"Project with name- {self.proj_name} deleted successfully. Test-case Pass.")
        else:
            assert proj_details, f"Project details not found to delete. Test-case Fail."