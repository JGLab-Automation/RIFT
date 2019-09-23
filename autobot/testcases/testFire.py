from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.lib import restAPIs as rapi
from autobot.config import constants as const
from autobot.config import payloads as pl
import unittest
import json
import os











#---------------------------------------
# transac_id = fw.pkg_onboard(const.lp_addr, const.header, const.proj_name_default, const.ping_vnfd_ext_url)
# state1 = fw.pkg_upload_status(const.lp_addr, const.header, const.proj_name_default, transac_id)
# util.log_info(f"Package onboard status: {state1}.")
#
# transac_id = fw.pkg_onboard(const.lp_addr, const.header, const.proj_name_default, const.pong_vnfd_ext_url)
# state2 = fw.pkg_upload_status(const.lp_addr, const.header, const.proj_name_default, transac_id)
# util.log_info(f"Package onboard status: {state2}.")
#
# transac_id = fw.pkg_onboard(const.lp_addr, const.header, const.proj_name_default, const.ping_pong_nsd_ext_url)
# state3 = fw.pkg_upload_status(const.lp_addr, const.header, const.proj_name_default, transac_id)
# util.log_info(f"Package onboard status: {state3}.")
#
# if state1 and state2 and state3 == "COMPLETED":
#     print(">>>>> All files are uploaded.")
#
# else:
#     assert state1 and state2 and state3 == "COMPLETED", ">>>> There's an issue!"
#---------------------------------------
# state1 = fw.pkg_delete(const.lp_addr, const.header, const.proj_name_default, "nsd", "ping_pong_nsd")
# state2 = fw.pkg_delete(const.lp_addr, const.header, const.proj_name_default, "vnfd", "pong_vnfd")
# state3 = fw.pkg_delete(const.lp_addr, const.header, const.proj_name_default, "vnfd", "ping_vnfd")
#
# if state1 and state2 and state3 == "OK":
#     print("All files are deleted,.")
#
#---------------------------------------


# class Test(unittest.TestCase):
#
#     def test01_test1(self):
#         util.log_info("This is test1.")
#         a = []
#         if a:
#             print("Not Empty!")
#         else:
#             assert a, "Empty!"
#
#     def test02_test2(self):
#         util.log_info("This is test2.")

#
# if __name__ == '__main__':
#     unittest.main()

# user, passwd, auth_url, tenant, mgmt_net, org,
#                           admin_user, admin_passwd, nsx_auth_url, nsx_user, nsx_passwd,
#                           vc_host, vc_port, vc_user, vc_passwd

# fw.cloud_acct_add(const.lp_addr, const.header, "default", "VCD_Test", "VMware-VCD", "500")
# fw.cloud_acct_config_vcd(const.lp_addr, const.header, "default", "VCD_Test", const.vim_vcd91_user, const.vim_vcd91_passwd,
#                          const.vim_vcd91_auth_url, const.vim_vcd91_tenant, const.vim_vcd91_mgmt_net, const.vim_vcd91_org,
#                          const.vim_vcd91_admin_user, const.vim_vcd91_admin_passwd,
#                          const.vim_vcd91_nsx_auth_url, const.vim_vcd91_nsx_user, const.vim_vcd91_nsx_passwd,
#                          const.vim_vcd91_vc_host, const.vim_vcd91_vc_port, const.vim_vcd91_vc_user, const.vim_vcd91_vc_passwd)
#

# x = fw.get_input_param_xpath(const.lp_addr, const.header, "default", "88e15856-6fb0-4ece-b76f-b42e39575110")
# print(type(x))
# for xp in range(len(x)):
#     print(x[xp]["xpath"])

proj_name=["default"]

#fw.vim_resource_discover(const.lp_addr, const.header, proj_name[0], const.cloud_acct_name)
# status = fw.vim_discovered_details(const.lp_addr, const.header, proj_name[0], const.cloud_acct_name)
#
# discovered_data = {"server": [], "interface": [], "network": []}
# util.log_info("Adding server details.")
# server_details = status["server"]
# util.log_info("Adding interface details.")
# interface_details = status["interface"]
# util.log_info("Adding network details.")
# network_details = status["network"]
#
# for items in server_details:
#     discovered_data["server"].append(items["name"])
# for items in interface_details:
#     discovered_data["interface"].append(items["name"])
# for items in network_details:
#     discovered_data["network"].append(items["name"])
#
# print(discovered_data)
#

# vdur_id = []
# vnfr = fw.get_vnfr_id(const.lp_addr, const.header, "auto")
# for ids in vnfr:
#     ids = fw.get_vdur_vim_id(const.lp_addr, const.header, "auto", ids)
#     for id in ids:
#         vdur_id.append(id)

# x = fw.get_vdu_name_id(const.lp_addr, const.header, "auto")
# print(x)

x = {'server': ['AutoOrigNS-HQjTJu84E-iovdu0', 'AutoOrigNS-HuukfM6Bg-iovdu0', 'Autobot2', 'Autobot1'], 'server_id': ['51512b6d-93b7-4253-9fdf-fa79ce6ecb9d', '5182662d-4a52-4670-bde1-f688c5101950', 'bd738d31-f6d0-4a52-906c-c48589870824', 'd88fe864-4f14-4bcb-907d-c1635ffe126c'], 'interface': ['test02_1__Auto_Orig_NS__ping_vnfd__1__ping_vnfd/cp1__ens4', 'test02_1__Auto_Orig_NS__pong_vnfd__2__pong_vnfd/cp1__ens4', '', 'test02_1__Auto_Orig_NS__pong_vnfd__2__pong_vnfd/cp0__ens3', '', 'test02_1__Auto_Orig_NS__ping_vnfd__1__ping_vnfd/cp0__ens3'], 'network': ['test02_1.Auto_Orig_NS.ping_pong_vld1', 'esc-net', 'PaloAlto HA Link', 'private', 'ribbon-private', 'public']}
# for items in x["server_id"]:
#     print(items)
# discovered_data = {"server": [], "server_id": [], "interface": [], "network": []}
# y = fw.get_vdu_name_id("10.110.5.2", const.header_default, "default")
# print(y)

a = fw.vim_discovered_details("10.110.5.2", const.header_default, "default", const.cloud_acct_name[0])

print(a)