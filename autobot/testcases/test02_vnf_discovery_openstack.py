__author__ = "JG"

import unittest
from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.config import constants as const


class ResourceDiscovery_OpenStack(unittest.TestCase):

    proj_name = ["test02_1", "test02_2"]
    proj_desc = "test01_resource_discovery_openstack"
    nsr_id = ["0", "e70d3746-2738-424d-9792-564ca8663153"]
    disc_details = {"server": [], "interface": [], "network": []}

    def test01_Project1_Add(self):
        util.log_info(f"Executing {self.test01_Project1_Add.__name__}.")

        fw.proj_add(const.lp_addr, const.header, self.proj_name[0], self.proj_desc)

        name = fw.get_proj_name(const.lp_addr, const.header, self.proj_name[0])
        if name == self.proj_name[0]:
            util.log_info(f"Project- {name}, added successfully. Test-case Pass.")
        else:
            assert name == self.proj_name[0], f"Expected- {self.proj_name[0]}, Configured- {name}. Test-case Fail."

    def test02_Project1_Configure(self):
        util.log_info(f"Executing {self.test02_Project1_Configure.__name__}.")

        fw.proj_config(const.lp_addr, const.header, self.proj_name[0], const.proj_user_name,
                       const.proj_user_domain, const.proj_role, const.proj_event_publish)

        config = fw.get_proj_user_role(const.lp_addr, const.header, self.proj_name[0])
        if config["role"] == "rw-project:project-admin":
            util.log_info(f"Project- {self.proj_name[0]} configured with user-role- {config['role']}. Test-case Pass.")
        else:
            assert config["role"] == "rw-project:project-admin", \
                f"Expected- rw-project:project-admin, Configured- {config['role']}. Test-case Fail."

    def test03_Cloud_Account_Add(self):
        util.log_info(f"Executing {self.test03_Cloud_Account_Add.__name__}.")

        fw.cloud_acct_add(const.lp_addr, const.header, self.proj_name[0], const.cloud_acct_name,
                          const.cloud_acct_type, const.cloud_acct_timeout)
        acct_type = fw.get_cloud_acct_type(const.lp_addr, const.header, self.proj_name[0], const.cloud_acct_name)
        if acct_type == "openstack":
            util.log_info(f"Account- {const.cloud_acct_name} added for account-type {acct_type}. Test-case Pass.")
        else:
            assert acct_type == "openstack", f"Expected- openstack, Configured- {acct_type}. Test-case Fail."

    def test04_Cloud_Account_Configure(self):
        util.log_info(f"Executing {self.test04_Cloud_Account_Configure.__name__}.")

        fw.cloud_acct_config_openstack(const.lp_addr, const.header, self.proj_name[0], const.cloud_acct_name,
                                       const.vim_os_key, const.vim_os_secret, const.vim_os_auth_url, const.vim_os_tenant
                                       )
        status = fw.cloud_acct_status(const.lp_addr, const.header, self.proj_name[0], const.cloud_acct_name)
        if status == "success":
            util.log_info(f"Cloud-account {const.cloud_acct_name} added successfully. Test-case Pass.")
        else:
            assert status == "success", f"Expected- success, Configured- {status}. Test-case Fail."

    def test05_Package_Onboard(self):
        util.log_info(f"Executing {self.test05_Package_Onboard.__name__}.")

        transac_id = fw.pkg_onboard(const.lp_addr, const.header, self.proj_name[0], const.ping_vnfd_ext_url)
        state1 = fw.pkg_upload_status(const.lp_addr, const.header, self.proj_name[0], transac_id)
        transac_id = fw.pkg_onboard(const.lp_addr, const.header, self.proj_name[0], const.pong_vnfd_ext_url)
        state2 = fw.pkg_upload_status(const.lp_addr, const.header, self.proj_name[0], transac_id)
        transac_id = fw.pkg_onboard(const.lp_addr, const.header, self.proj_name[0], const.ping_pong_nsd_ext_url)
        state3 = fw.pkg_upload_status(const.lp_addr, const.header, self.proj_name[0], transac_id)

        if state1 and state2 and state3 == "COMPLETED":
            util.log_info(f"Ping VNFD, Pong VNFD & Ping_Pong NSD are uploaded in project- {self.proj_name[0]}. "
                          f"Test-case Pass.")
        else:
            assert state1 and state2 and state3 == "COMPLETED", f"Expected- COMPLETED, Received- {state1, state2, state3}. " \
                f"Test-case Fail."

    def test06_NS_Create(self):
        util.log_info(f"Executing {self.test06_NS_Create.__name__}.")

        ns_name = "AutoTest"
        nsd = fw.get_nsd_name_id(const.lp_addr, const.header, self.proj_name[0])
        nsd_id = nsd["ping_pong_nsd"]
        nsr_id = fw.ns_create(const.lp_addr, const.header, self.proj_name[0], ns_name, nsd_id)
        self.nsr_id.append(nsr_id)

        conf_name = fw.get_ns_instance_config(const.lp_addr, const.header, self.proj_name[0], self.nsr_id[0], "name")
        conf_state = fw.get_ns_instance_config(const.lp_addr, const.header, self.proj_name[0], self.nsr_id[0], "status")

        if conf_name == ns_name and conf_state == "DISABLED":
            util.log_info(f"NS is created with name- {conf_name} and current state is- {conf_state}. Test-case Pass.")
        else:
            assert conf_name == ns_name and conf_state == "DISABLED", \
                f"Expected name- {ns_name}, Configured name- {conf_name}. Test-case Fail."

    def test07_NS_Instantiate(self):
        util.log_info(f"Executing {self.test07_NS_Instantiate.__name__}.")

        fw.ns_instantiate(const.lp_addr, const.header, self.proj_name[0], self.nsr_id[0])
        conf_state = fw.get_ns_instance_config(const.lp_addr, const.header, self.proj_name[0], self.nsr_id[0], "status")
        state = fw.get_ns_oper_status(const.lp_addr, const.header, self.proj_name[0], self.nsr_id[0])
        if conf_state == "ENABLED" and state == "running":
            util.log_info(f"NS with ID- {self.nsr_id[0]} instantiated successfully and is- {state}. Test-case Pass.")
        else:
            assert conf_state == "ENABLED" and state == "running", \
                f"Expected state- running, Current state- {state}. Test-case Fail."

    def test08_Project2_Add(self):
        util.log_info(f"Executing {self.test08_Project2_Add.__name__}.")

        fw.proj_add(const.lp_addr, const.header, self.proj_name[1], self.proj_desc)

        name = fw.get_proj_name(const.lp_addr, const.header, self.proj_name[1])
        if name == self.proj_name[1]:
            util.log_info(f"Project- {name}, added successfully. Test-case Pass.")
        else:
            assert name == self.proj_name[1], f"Expected- {self.proj_name[1]}, Configured- {name}. Test-case Fail."

    def test09_Project2_Configure(self):
        util.log_info(f"Executing {self.test09_Project2_Configure.__name__}.")

        fw.proj_config(const.lp_addr, const.header, self.proj_name[1], const.proj_user_name,
                       const.proj_user_domain, const.proj_role, const.proj_event_publish)

        config = fw.get_proj_user_role(const.lp_addr, const.header, self.proj_name[1])
        if config["role"] == "rw-project:project-admin":
            util.log_info(f"Project- {self.proj_name[1]} configured with user-role- {config['role']}. Test-case Pass.")
        else:
            assert config["role"] == "rw-project:project-admin", \
                f"Expected- rw-project:project-admin, Configured- {config['role']}. Test-case Fail."

    def test10_Cloud_Account_Add(self):
        util.log_info(f"Executing {self.test10_Cloud_Account_Add.__name__}.")

        fw.cloud_acct_add(const.lp_addr, const.header, self.proj_name[1], const.cloud_acct_name,
                          const.cloud_acct_type, const.cloud_acct_timeout)
        acct_type = fw.get_cloud_acct_type(const.lp_addr, const.header, self.proj_name[1], const.cloud_acct_name)
        if acct_type == "openstack":
            util.log_info(f"Account- {const.cloud_acct_name} added for account-type {acct_type}. Test-case Pass.")
        else:
            assert acct_type == "openstack", f"Expected- openstack, Configured- {acct_type}. Test-case Fail."

    def test11_Cloud_Account_Configure(self):
        util.log_info(f"Executing {self.test11_Cloud_Account_Configure.__name__}.")

        fw.cloud_acct_config_openstack(const.lp_addr, const.header, self.proj_name[1], const.cloud_acct_name,
                                       const.vim_os_key, const.vim_os_secret, const.vim_os_auth_url, const.vim_os_tenant
                                       )
        status = fw.cloud_acct_status(const.lp_addr, const.header, self.proj_name[1], const.cloud_acct_name)
        if status == "success":
            util.log_info(f"Cloud-account {const.cloud_acct_name} added successfully. Test-case Pass.")
        else:
            assert status == "success", f"Expected- success, Configured- {status}. Test-case Fail."

    def test12_Package_Onboard(self):
        util.log_info(f"Executing {self.test12_Package_Onboard.__name__}.")

        transac_id = fw.pkg_onboard(const.lp_addr, const.header, self.proj_name[1], const.ping_vnfd_ext_url)
        state1 = fw.pkg_upload_status(const.lp_addr, const.header, self.proj_name[1], transac_id)
        transac_id = fw.pkg_onboard(const.lp_addr, const.header, self.proj_name[1], const.pong_vnfd_ext_url)
        state2 = fw.pkg_upload_status(const.lp_addr, const.header, self.proj_name[1], transac_id)
        transac_id = fw.pkg_onboard(const.lp_addr, const.header, self.proj_name[1], const.ping_pong_nsd_ext_url)
        state3 = fw.pkg_upload_status(const.lp_addr, const.header, self.proj_name[1], transac_id)

        if state1 and state2 and state3 == "COMPLETED":
            util.log_info(f"Ping VNFD, Pong VNFD & Ping_Pong NSD are uploaded in project- {self.proj_name[1]}. "
                          f"Test-case Pass.")
        else:
            assert state1 and state2 and state3 == "COMPLETED", f"Expected- COMPLETED, Received- {state1, state2, state3}. " \
                f"Test-case Fail."

    def test13_Discover_Resource(self):
        util.log_info(f"Executing {self.test13_Discover_Resource().__name__}.")

        fw.vim_resource_discover(const.lp_addr, const.header, self.proj_name[1], const.cloud_acct_name)
        status = fw.vim_discover_status(const.lp_addr, const.header, self.proj_name[1], const.cloud_acct_name)
        if status == "discovered":
            util.log_info(f"Resource discovery on account-name- {const.cloud_acct_name} is successful. Test-case Pass.")
        else:
            assert status == "discovered", f"Expected- success, Configured- {status}. Test-case Fail."

    def test14_Collect_Discovered_Details(self):
        util.log_info(f"Executing {self.test13_Discover_Resource().__name__}.")

        status = fw.vim_discovered_details(const.lp_addr, const.header, self.proj_name[1], const.cloud_acct_name)
        if status:
            util.log_info("Adding server details.")
            server_details = status["server"]
            util.log_info("Adding interface details.")
            interface_details = status["interface"]
            util.log_info("Adding network details.")
            network_details = status["network"]
            for items in server_details:
                self.disc_details["server"].append(items["name"])
            for items in interface_details:
                self.disc_details["interface"].append(items["name"])
            for items in network_details:
                self.disc_details["network"].append(items["name"])
        else:
            assert status, f"Status is {status}. Test-case Fail."

    def test15_NS_Create(self):
        util.log_info(f"Executing {self.test15_NS_Create.__name__}.")

        ns_name = "AutoTest"
        nsd = fw.get_nsd_name_id(const.lp_addr, const.header, self.proj_name[1])
        nsd_id = nsd["ping_pong_nsd"]
        nsr_id = fw.ns_create(const.lp_addr, const.header, self.proj_name[1], ns_name, nsd_id)
        self.nsr_id.append(nsr_id)

        conf_name = fw.get_ns_instance_config(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1], "name")
        conf_state = fw.get_ns_instance_config(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1], "status")

        if conf_name == ns_name and conf_state == "DISABLED":
            util.log_info(f"NS is created with name- {conf_name} and current state is- {conf_state}. Test-case Pass.")
        else:
            assert conf_name == ns_name and conf_state == "DISABLED", \
                f"Expected name- {ns_name}, Configured name- {conf_name}. Test-case Fail."

    def test16_Add_Discovered_Resources(self):
        util.log_info(f"Executing {self.test16_Add_Discovered_Resources.__name__}.")

        xp1 = "/connect-vnf[1]/vdur[vdu-id-ref='iovdu_0']/preexisting-resource-name"
        xp2 = "/connect-vnf[2]/vdur[vdu-id-ref='iovdu_0']/preexisting-resource-name"
        xp3 = "/connect-vnf[1]/vdur[vdu-id-ref='iovdu_0']/interface[name='ens3']/preexisting-resource-name"
        xp4 = "/connect-vnf[1]/vdur[vdu-id-ref='iovdu_0']/interface[name='ens4']/preexisting-resource-name"
        xp5 = "/connect-vnf[2]/vdur[vdu-id-ref='iovdu_0']/interface[name='ens3']/preexisting-resource-name"
        xp6 = "/connect-vnf[2]/vdur[vdu-id-ref='iovdu_0']/interface[name='ens4']/preexisting-resource-name"
        xp7 = "/nsd/vld[id='ping_pong_vld1']/vim-network-name"

        fw.add_input_param_xpath(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1],
                                 xp1, self.disc_details["server"][1])
        fw.add_input_param_xpath(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1],
                                 xp2, self.disc_details["server"][0])
        fw.add_input_param_xpath(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1],
                                 xp3, self.disc_details["interface"][2])
        fw.add_input_param_xpath(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1],
                                 xp4, self.disc_details["interface"][3])
        fw.add_input_param_xpath(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1],
                                 xp5, self.disc_details["interface"][0])
        fw.add_input_param_xpath(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1],
                                 xp6, self.disc_details["interface"][1])
        fw.add_input_param_xpath(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1],
                                 xp7, self.disc_details["network"][0])

        util.log_info(f"Checking if xpaths are added to NSR: {self.nsr_id[1]}.")
        xps = fw.get_input_param_xpath(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1])
        if len(xps) >= 7:
            util.log_info(f"Total {len(xps)} xPaths are available.")
        else:
            assert len(xps) >= 7, f"Expected- >= 7, Added- {len(xps)}. Test-case Fail."

    def test17_NS_Instantiate(self):
        util.log_info(f"Executing {self.test17_NS_Instantiate.__name__}.")

        fw.ns_instantiate(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1])
        conf_state = fw.get_ns_instance_config(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1], "status")
        state = fw.get_ns_oper_status(const.lp_addr, const.header, self.proj_name[1], self.nsr_id[1])
        if conf_state == "ENABLED" and state == "running":
            util.log_info(f"NS with ID- {self.nsr_id[1]} instantiated successfully and is- {state}. Test-case Pass.")
        else:
            assert conf_state == "ENABLED" and state == "running", \
                f"Expected state- running, Current state- {state}. Test-case Fail."

