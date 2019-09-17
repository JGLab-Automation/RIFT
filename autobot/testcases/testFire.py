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

fw.cloud_acct_add(const.lp_addr, const.header, "default", "VCD_Test", "VMware-VCD", "500")
fw.cloud_acct_config_vcd(const.lp_addr, const.header, "default", "VCD_Test", const.vim_vcd91_user, const.vim_vcd91_passwd,
                         const.vim_vcd91_auth_url,const.vim_vcd91_tenant, const.vim_vcd91_mgmt_net, const.vim_vcd91_org,
                         const.vim_vcd91_admin_user, const.vim_vcd91_admin_passwd,
                         const.vim_vcd91_nsx_auth_url, const.vim_vcd91_nsx_user, const.vim_vcd91_nsx_passwd,
                         const.vim_vcd91_vc_host, const.vim_vcd91_vc_port, const.vim_vcd91_vc_user, const.vim_vcd91_vc_passwd)

