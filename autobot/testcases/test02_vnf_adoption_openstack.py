__author__ = "JG"

import unittest
from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.config import constants as const


class VNFAdoptionOpenStack(unittest.TestCase):

    proj_name = ["test02_1", "test02_2"]
    proj_desc = "test02_vnf_adoption_openstack"
    nsr_id = []
    discovered_data = {"server": [], "server_id": [], "interface": [], "network": []}
    xpath_values = {"server": {"ping": "", "pong": ""},
                    "interface": {"ping_ens3": "", "ping_ens4": "", "pong_ens3": "", "pong_ens4": ""},
                    "network": {"ping_pong": ""}}

    def test01_Project1_Add(self):
        util.log_info(f"Executing {self.test01_Project1_Add.__name__}.")

        fw.proj_add(const.lp_addr_default[0], const.header_default, self.proj_name[0], self.proj_desc)

        name = fw.get_proj_name(const.lp_addr_default[0], const.header_default, self.proj_name[0])
        if name == self.proj_name[0]:
            util.log_info(f"Project- {name}, added successfully. Test-case Pass.")
        else:
            util.log_info(f"Expected- {self.proj_name[0]}, Actual- {name}. Test-case Fail.")
            assert name == self.proj_name[0], f"Expected- {self.proj_name[0]}, Actual- {name}. Test-case Fail."

    def test02_Project1_Configure(self):
        util.log_info(f"Executing {self.test02_Project1_Configure.__name__}.")

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
            util.log_info(f"Expected- openstack, Actual- {acct_type}. Test-case Fail.")
            assert acct_type == "openstack", f"Expected- openstack, Actual- {acct_type}. Test-case Fail."

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
            util.log_info(f"Expected- success, Actual- {status}. Test-case Fail.")
            assert status == "success", f"Expected- success, Actual- {status}. Test-case Fail."

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

        ns_name = "Auto_Orig_NS"
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

    def test08_Project2_Add(self):
        util.log_info(f"Executing {self.test08_Project2_Add.__name__}.")

        fw.proj_add(const.lp_addr_default[0], const.header_default, self.proj_name[1], self.proj_desc)

        name = fw.get_proj_name(const.lp_addr_default[0], const.header_default, self.proj_name[1])
        if name == self.proj_name[1]:
            util.log_info(f"Project- {name}, added successfully. Test-case Pass.")
        else:
            util.log_info(f"Expected- {self.proj_name[1]}, Actual- {name}. Test-case Fail.")
            assert name == self.proj_name[1], f"Expected- {self.proj_name[1]}, Actual- {name}. Test-case Fail."

    def test09_Project2_Configure(self):
        util.log_info(f"Executing {self.test09_Project2_Configure.__name__}.")

        fw.proj_config(const.lp_addr_default[0], const.header_default, self.proj_name[1], const.proj_user_name,
                       const.proj_user_domain, const.proj_role, const.proj_event_publish)

        config = fw.get_proj_user_role(const.lp_addr_default[0], const.header_default, self.proj_name[1])
        if config["role"] == "rw-project:project-admin":
            util.log_info(f"Project- {self.proj_name[1]} configured with user-role- {config['role']}. Test-case Pass.")
        else:
            util.log_info(f"Expected- rw-project:project-admin, Configured- {config['role']}. Test-case Fail.")
            assert config["role"] == "rw-project:project-admin", \
                f"Expected- rw-project:project-admin, Configured- {config['role']}. Test-case Fail."

    def test10_Cloud_Account_Add(self):
        util.log_info(f"Executing {self.test10_Cloud_Account_Add.__name__}.")

        fw.cloud_acct_add(const.lp_addr_default[0], const.header_default, self.proj_name[1], const.cloud_acct_name[0],
                          const.cloud_acct_type[0], const.cloud_acct_timeout[0])
        acct_type = fw.get_cloud_acct_type(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                           const.cloud_acct_name[0])
        if acct_type == "openstack":
            util.log_info(f"Account- {const.cloud_acct_name[0]} added for account-type {acct_type}. Test-case Pass.")
        else:
            util.log_info(f"Expected- openstack, Actual- {acct_type}. Test-case Fail.")
            assert acct_type == "openstack", f"Expected- openstack, Actual- {acct_type}. Test-case Fail."

    def test11_Cloud_Account_Configure(self):
        util.log_info(f"Executing {self.test11_Cloud_Account_Configure.__name__}.")

        fw.cloud_acct_config_openstack(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                       const.cloud_acct_name[0], const.vim_os_key, const.vim_os_secret,
                                       const.vim_os_auth_url, const.vim_os_tenant)
        status = fw.cloud_acct_status(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                      const.cloud_acct_name[0])
        if status == "success":
            util.log_info(f"Cloud-account {const.cloud_acct_name[0]} added successfully. Test-case Pass.")
        else:
            util.log_info(f"Expected- success, Actual- {status}. Test-case Fail.")
            assert status == "success", f"Expected- success, Actual- {status}. Test-case Fail."

    def test12_Package_Onboard(self):
        util.log_info(f"Executing {self.test12_Package_Onboard.__name__}.")

        transac_id = fw.pkg_onboard(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                    const.ping_vnfd_ext_url)
        state1 = fw.pkg_upload_status(const.lp_addr_default[0], const.header_default, self.proj_name[1], transac_id)
        transac_id = fw.pkg_onboard(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                    const.pong_vnfd_ext_url)
        state2 = fw.pkg_upload_status(const.lp_addr_default[0], const.header_default, self.proj_name[1], transac_id)
        transac_id = fw.pkg_onboard(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                    const.ping_pong_nsd_ext_url)
        state3 = fw.pkg_upload_status(const.lp_addr_default[0], const.header_default, self.proj_name[1], transac_id)

        if state1 and state2 and state3 == "COMPLETED":
            util.log_info(f"Ping VNFD, Pong VNFD & Ping_Pong NSD are uploaded in project- {self.proj_name[1]}. "
                          f"Test-case Pass.")
        else:
            util.log_info(f"Expected- COMPLETED, Received- {state1, state2, state3}. Test-case Fail.")
            assert state1 and state2 and state3 == "COMPLETED", \
                f"Expected- COMPLETED, Received- {state1, state2, state3}. Test-case Fail."

    def test13_Discover_Resource(self):
        util.log_info(f"Executing {self.test13_Discover_Resource.__name__}.")

        fw.vim_resource_discover(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                 const.cloud_acct_name[0])
        status = fw.vim_discover_status(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                        const.cloud_acct_name[0])
        if status == "discovered":
            util.log_info(f"Resource discovery on account-name- {const.cloud_acct_name[0]} is successful. "
                          f"Test-case Pass.")
        else:
            util.log_info(f"Expected- success, Actual- {status}. Test-case Fail.")
            assert status == "discovered", f"Expected- success, Actual- {status}. Test-case Fail."

    def test14_Collect_Discovered_Details(self):
        util.log_info(f"Executing {self.test14_Collect_Discovered_Details.__name__}.")

        util.log_info("Collecting Server, Interface & Network details from discovered-resource.")
        status = fw.vim_discovered_details(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                           const.cloud_acct_name[0])
        if status:
            util.log_info("Adding server details.")
            server_details = status["server"]
            util.log_info("Adding interface details.")
            interface_details = status["interface"]
            util.log_info("Adding network details.")
            network_details = status["network"]
            for items in server_details:
                self.discovered_data["server"].append(items["name"])
            for items in server_details:
                self.discovered_data["server_id"].append(items["id"])
            for items in interface_details:
                self.discovered_data["interface"].append(items["name"])
            for items in network_details:
                self.discovered_data["network"].append(items["name"])
            util.log_info(f"Discovered resources- {self.discovered_data}.")

            util.log_info("Collecting NSR-VNFR details.")
            vdu = fw.get_vdu_name_id(const.lp_addr_default[0], const.header_default, self.proj_name[0])

            util.log_info("Mapping server details.")
            for items in self.discovered_data["server_id"]:
                if vdu["ping_vnfd"] == self.discovered_data["server_id"][0] and vdu["ping_vnfd"] == items:
                    self.xpath_values["server"].update({"ping": self.discovered_data["server"][0]})
                if vdu["ping_vnfd"] == self.discovered_data["server_id"][1] and vdu["ping_vnfd"] == items:
                    self.xpath_values["server"].update({"ping": self.discovered_data["server"][1]})
                if vdu["pong_vnfd"] == self.discovered_data["server_id"][0] and vdu["pong_vnfd"] == items:
                    self.xpath_values["server"].update({"pong": self.discovered_data["server"][0]})
                if vdu["pong_vnfd"] == self.discovered_data["server_id"][1] and vdu["pong_vnfd"] == items:
                    self.xpath_values["server"].update({"ping": self.discovered_data["server"][1]})

            util.log_info("Mapping connection-points details.")
            for items in self.discovered_data["interface"]:
                cps = items.split("_")
                for vnfd in cps:
                    for cp in cps:
                        if vnfd == "ping" and cp == "ens3":
                            self.xpath_values["interface"].update({"ping_ens3": items})
                        if vnfd == "ping" and cp == "ens4":
                            self.xpath_values["interface"].update({"ping_ens4": items})
                        if vnfd == "pong" and cp == "ens3":
                            self.xpath_values["interface"].update({"pong_ens3": items})
                        if vnfd == "pong" and cp == "ens4":
                            self.xpath_values["interface"].update({"pong_ens4": items})

            util.log_info("Mapping network details.")
            for items in self.discovered_data["network"]:
                networks = items.split(".")
                for proj in networks:
                    for net2 in networks:
                        if proj == self.proj_name[0] and net2 == "ping_pong_vld1":
                            self.xpath_values["network"].update({"ping_pong": items})

            util.log_info(f"xPath mappings- {self.xpath_values}.")

        else:
            util.log_info(f"Status is {status}. Test-case Fail.")
            assert status, f"Status is {status}. Test-case Fail."

    def test15_Add_Discovered_Resources(self):
        util.log_info(f"Executing {self.test15_Add_Discovered_Resources.__name__}.")

        xp1 = "/connect-vnf[1]/vdur[vdu-id-ref='iovdu_0']/preexisting-resource-name"
        xp2 = "/connect-vnf[2]/vdur[vdu-id-ref='iovdu_0']/preexisting-resource-name"
        xp3 = "/connect-vnf[1]/vdur[vdu-id-ref='iovdu_0']/interface[name='ens3']/preexisting-resource-name"
        xp4 = "/connect-vnf[1]/vdur[vdu-id-ref='iovdu_0']/interface[name='ens4']/preexisting-resource-name"
        xp5 = "/connect-vnf[2]/vdur[vdu-id-ref='iovdu_0']/interface[name='ens3']/preexisting-resource-name"
        xp6 = "/connect-vnf[2]/vdur[vdu-id-ref='iovdu_0']/interface[name='ens4']/preexisting-resource-name"
        xp7 = "/nsd/vld[id='ping_pong_vld1']/vim-network-name"
        xp8 = "/nsd/vendor"

        nsd_id = fw.get_nsd_id(const.lp_addr_default[0], const.header_default, self.proj_name[1])
        util.log_info(f"Adding discovered values to xPaths in NSD- {nsd_id[0]}.")

        fw.add_input_param_xpath_nsd(const.lp_addr_default[0], const.header_default, self.proj_name[1], nsd_id[0],
                                     xp1, self.xpath_values["server"]["ping"])
        fw.add_input_param_xpath_nsd(const.lp_addr_default[0], const.header_default, self.proj_name[1], nsd_id[0],
                                     xp2, self.xpath_values["server"]["pong"])

        fw.add_input_param_xpath_nsd(const.lp_addr_default[0], const.header_default, self.proj_name[1], nsd_id[0],
                                     xp3, self.xpath_values["interface"]["ping_ens3"])
        fw.add_input_param_xpath_nsd(const.lp_addr_default[0], const.header_default, self.proj_name[1], nsd_id[0],
                                     xp4, self.xpath_values["interface"]["ping_ens4"])
        fw.add_input_param_xpath_nsd(const.lp_addr_default[0], const.header_default, self.proj_name[1], nsd_id[0],
                                     xp5, self.xpath_values["interface"]["pong_ens3"])
        fw.add_input_param_xpath_nsd(const.lp_addr_default[0], const.header_default, self.proj_name[1], nsd_id[0],
                                     xp6, self.xpath_values["interface"]["pong_ens4"])

        fw.add_input_param_xpath_nsd(const.lp_addr_default[0], const.header_default, self.proj_name[1], nsd_id[0],
                                     xp7, self.xpath_values["network"]["ping_pong"])

        util.log_info("Deleting unwanted xPath(s) for this feature.")
        fw.delete_input_param_xpath_nsd(const.lp_addr_default[0], const.header_default, self.proj_name[1], nsd_id[0],
                                     xp8)

        util.log_info(f"Checking if xPaths are added to NSD- {nsd_id[0]}.")
        xps = fw.get_input_param_xpath_nsd(const.lp_addr_default[0], const.header_default, self.proj_name[1], nsd_id[0])
        if len(xps) >= 7:
            util.log_info(f"Total {len(xps)} xPaths are available.")
        else:
            util.log_info(f"Expected- >= 7, Added- {len(xps)}. Test-case Fail.")
            assert len(xps) >= 7, f"Expected- >= 7, Added- {len(xps)}. Test-case Fail."

    def test16_NS_Create(self):
        util.log_info(f"Executing {self.test16_NS_Create.__name__}.")

        ns_name = "Auto_Adopted_NS"
        nsd = fw.get_nsd_name_id(const.lp_addr_default[0], const.header_default, self.proj_name[1])
        nsd_id = nsd["ping_pong_nsd"]
        nsr_id = fw.ns_create(const.lp_addr_default[0], const.header_default, self.proj_name[1], ns_name, nsd_id)
        self.nsr_id.append(nsr_id)

        conf_name = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                              self.nsr_id[1], "name")
        conf_state = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                               self.nsr_id[1], "status")

        if conf_name == ns_name and conf_state == "DISABLED":
            util.log_info(f"NS is created with name- {conf_name} and current state is- {conf_state}. Test-case Pass.")
        else:
            util.log_info(f"Expected name- {ns_name}, Configured name- {conf_name}. Test-case Fail.")
            assert conf_name == ns_name and conf_state == "DISABLED", \
                f"Expected name- {ns_name}, Configured name- {conf_name}. Test-case Fail."

    def test17_NS_Instantiate(self):
        util.log_info(f"Executing {self.test17_NS_Instantiate.__name__}.")

        fw.ns_instantiate(const.lp_addr_default[0], const.header_default, self.proj_name[1], self.nsr_id[1])
        conf_state = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                               self.nsr_id[1], "status")
        state = fw.get_ns_oper_status(const.lp_addr_default[0], const.header_default, self.proj_name[1], self.nsr_id[1])
        if conf_state == "ENABLED" and state == "running":
            util.log_info(f"NS with ID- {self.nsr_id[1]} instantiated successfully and is- {state}. Test-case Pass.")
        else:
            util.log_info(f"Expected state- running, Current state- {state}. Test-case Fail.")
            assert conf_state == "ENABLED" and state == "running", \
                f"Expected state- running, Current state- {state}. Test-case Fail."

    def test18_NS_Terminate(self):
        util.log_info(f"Executing {self.test18_NS_Terminate.__name__}.")

        state = fw.get_ns_oper_status(const.lp_addr_default[0], const.header_default, self.proj_name[1], self.nsr_id[1])
        if state == "running":
            fw.ns_terminate(const.lp_addr_default[0], const.header_default, self.proj_name[1], self.nsr_id[1])
            conf_state = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                                   self.nsr_id[1], "status")
            state = fw.get_ns_oper_status(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                          self.nsr_id[1])
            if conf_state == "DISABLED" and state == "terminated":
                util.log_info(f"NS with NSR ID- {self.nsr_id[1]} terminated successfully. Test-case Pass.")
            else:
                util.log_info(f"Expected state- terminated, Current state- {state}. Test-case Fail.")
                assert conf_state == "DISABLED" and state == "terminated", \
                    f"Expected state- terminated, Current state- {state}. Test-case Fail."
        else:
            util.log_info(f"Current state- {state}. Test-case Fail.")
            assert state == "running", f"NS with NSR ID- {self.nsr_id[1]} is not running. " \
                f"Current state- {state}. Test-case Fail."

    def test19_NS_Delete(self):
        util.log_info(f"Executing {self.test19_NS_Delete.__name__}.")

        conf_state = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                               self.nsr_id[1], "status")
        state = fw.get_ns_oper_status(const.lp_addr_default[0], const.header_default, self.proj_name[1], self.nsr_id[1])
        if conf_state == "DISABLED" or state == "terminated":
            fw.ns_delete(const.lp_addr_default[0], const.header_default, self.proj_name[1], self.nsr_id[1])
            conf_state = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                                   self.nsr_id[1])
            if not conf_state:
                util.log_info(f"NS with NSR ID- {self.nsr_id[1]} deleted successfully. Test-case Pass.")
            else:
                util.log_info(f"NS with NSR ID- {self.nsr_id[1]} is not deleted. "
                              f"NS still has config-data- {conf_state}. Test-case Fail.")
                assert not conf_state, f"NS with NSR ID- {self.nsr_id[1]} is not deleted. " \
                    f"NS still has config-data- {conf_state}. Test-case Fail."
        else:
            util.log_info(f"NS with NSR ID- {self.nsr_id[1]} is not terminated. Current state- {state}. "
                          f"Test-case Fail.")
            assert conf_state == "DISABLED" or state == "terminated",\
                f"NS with NSR ID- {self.nsr_id[1]} is not terminated. Current state- {state}. Test-case Fail."

    def test20_Package_Delete(self):
        util.log_info(f"Executing {self.test20_Package_Delete.__name__}.")

        pkg_catalog = fw.get_pkg_catalog(const.lp_addr_default[0], const.header_default, self.proj_name[1])
        if pkg_catalog:
            fw.pkg_delete(const.lp_addr_default[0], const.header_default, self.proj_name[1], "nsd", "ping_pong_nsd")
            fw.pkg_delete(const.lp_addr_default[0], const.header_default, self.proj_name[1], "vnfd", "pong_vnfd")
            fw.pkg_delete(const.lp_addr_default[0], const.header_default, self.proj_name[1], "vnfd", "ping_vnfd")

            pkg_catalog = fw.get_pkg_catalog(const.lp_addr_default[0], const.header_default, self.proj_name[1])
            if pkg_catalog is None:
                util.log_info("Packages deleted successfully. Test-case Pass.")
            else:
                util.log_info("Packages couldn't delete successfully. Test-case Fail.")
                assert pkg_catalog is None, "Packages couldn't delete successfully. Test-case Fail."
        else:
            util.log_info(f"Packages not available to delete. Test-case Fail.")
            assert pkg_catalog, f"Packages not available to delete. Test-case Fail."

    def test21_Cloud_Account_Delete(self):
        util.log_info(f"Executing {self.test21_Cloud_Account_Delete.__name__}.")

        acct = fw.get_cloud_acct_details(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                         const.cloud_acct_name[0])
        if acct:
            fw.cloud_acct_delete(const.lp_addr_default[0], const.header_default, self.proj_name[1],
                                 const.cloud_acct_name[0])
            acct = fw.get_cloud_acct_details(const.lp_addr_default[0], const.header_default, self.proj_name[1],
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

    def test22_Project2_Delete(self):
        util.log_info(f"Executing {self.test22_Project2_Delete.__name__}.")

        proj_details = fw.get_proj_details(const.lp_addr_default[0], const.header_default, self.proj_name[1])
        if proj_details:
            fw.proj_delete(const.lp_addr_default[0], const.header_default, self.proj_name[1])
            proj_details = fw.get_proj_details(const.lp_addr_default[0], const.header_default, self.proj_name[1])
            if proj_details is None:
                util.log_info(f"Project with name- {self.proj_name[1]} deleted successfully. Test-case Pass.")
            else:
                util.log_info(f"Expected- None, Actual- {proj_details}. Test-case Fail.")
                assert proj_details is None, f"Expected- None, Actual- {proj_details}. Test-case Fail."
        else:
            util.log_info(f"Project details not found to delete. Test-case Fail.")
            assert proj_details, f"Project details not found to delete. Test-case Fail."

    def test23_NS_Terminate(self):
        util.log_info(f"Executing {self.test23_NS_Terminate.__name__}.")

        state = fw.get_ns_oper_status(const.lp_addr_default[0], const.header_default, self.proj_name[0], self.nsr_id[0])
        if state == "running":
            fw.ns_terminate(const.lp_addr_default[0], const.header_default, self.proj_name[0], self.nsr_id[0])
            conf_state = fw.get_ns_instance_config(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                                   self.nsr_id[0], "status")
            state = fw.get_ns_oper_status(const.lp_addr_default[0], const.header_default, self.proj_name[0],
                                          self.nsr_id[0])
            if conf_state == "DISABLED" and state == "terminated":
                util.log_info(f"NS with NSR ID- {self.nsr_id[1]} terminated successfully. Test-case Pass.")
            else:
                util.log_info(f"Expected state- terminated, Current state- {state}. Test-case Fail.")
                assert conf_state == "DISABLED" and state == "terminated", \
                    f"Expected state- terminated, Current state- {state}. Test-case Fail."
        else:
            util.log_info(f"NS with NSR ID- {self.nsr_id[1]} is not running. Current state- {state}. "
                          f"Test-case Fail.")
            assert state == "running", f"NS with NSR ID- {self.nsr_id[1]} is not running. Current state- {state} " \
                f"Test-case Fail."

    def test24_NS_Delete(self):
        util.log_info(f"Executing {self.test24_NS_Delete.__name__}.")

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
            util.log_info(f"NS with NSR ID- {self.nsr_id[1]} is not terminated. Current state- {state}. "
                          f"Test-case Fail.")
            assert conf_state == "DISABLED" or state == "terminated", \
                f"NS with NSR ID- {self.nsr_id[1]} is not terminated. Current state- {state}. Test-case Fail."

    def test25_Package_Delete(self):
        util.log_info(f"Executing {self.test25_Package_Delete.__name__}.")

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

    def test26_Cloud_Account_Delete(self):
        util.log_info(f"Executing {self.test26_Cloud_Account_Delete.__name__}.")

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
                assert not acct, f"Cloud account with name- {const.cloud_acct_name[0]} couldn't get deleted." \
                    f"Test-case Fail."
        else:
            util.log_info(f"Cloud account with name- {const.cloud_acct_name[0]} is not configured. Test-case Fail.")
            assert acct, f"Cloud account with name- {const.cloud_acct_name[0]} is not configured. Test-case Fail."

    def test27_Project1_Delete(self):
        util.log_info(f"Executing {self.test27_Project1_Delete.__name__}.")

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
            util.log_info("Project details not found to delete. Test-case Fail.")
            assert proj_details, f"Project details not found to delete. Test-case Fail."


if __name__ == '__main__':
    unittest.main()
