from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.lib import restAPIs as rapi
from autobot.config import constants as const
from autobot.config import payloads as pl
import json

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
"""
{
	"input":
	{
		"project-name":"Test1",
		"name":"Test2",
		"nsd-id-ref":"cc12e5cc-a650-11e9-b8ce-02420a40cc02"
		
	}
	
}


{'output': {'nsr-id': 'a4c71a86-eaa4-4366-b6ce-e7b7b1162245', 'transaction-status': 'init', 'transaction-id': 'b373710e-d462-11e9-8e3d-02420a6e0502'}}
"""

# ns_name = "AutoTest7"
# nsd = fw.get_nsd_name_id(const.lp_addr, const.header, const.proj_name_default)
# nsd_id = nsd["ping_pong_nsd"]
# print("-"*10)
# print(nsd_id)
# print("-"*10)
# nsr_id, state = fw.ns_add(const.lp_addr, const.header, const.proj_name_default, ns_name, nsd_id)
# print("-"*10)
# print(nsr_id)
# print("-"*10)
#nsr_id = "89b93d7b-20ef-431e-94b0-f8a1875df1c8"
#state = fw.ns_terminate(const.lp_addr, const.header, const.proj_name_default, nsr_id)
# status = fw.get_ns_oper_status(const.lp_addr, const.header, const.proj_name_default, nsr_id)
# print(status)

# status = fw.get_ns_oper_status(const.lp_addr, const.header, const.proj_name_default, nsr_id)
# if status == "terminated":
#     state = fw.ns_delete(const.lp_addr, const.header, const.proj_name_default, nsr_id)
#     print(state)
#
#

x = fw.get_proj_name(const.lp_addr, const.header, const.proj_name_default)
print(x)











#
# x = "{\"input\":{\"project-name\":\"Test1\",\"nsr-id-ref\":\"7b3607ec-33d5-47e0-a603-52ef87ce4b20\"}}"
# print(json.loads(x))

# x = "{\"input\":{\"nsr-id-ref\":\"a4c71a86-eaa4-4366-b6ce-e7b7b1162245\",\"deployment-profile\":{\"config-timeout\":1200,\"auto-rollback\":\"DISABLED\",\"ip-profile-map\":[{\"ip-profile-ref\":\"InterVNFLink-1\",\"ip-profile-params\":{\"subnet\":[{\"name\":\"subnet-1\",\"ip-version\":\"ipv4\",\"subnet-address\":\"31.31.31.0/24\",\"dhcp-params\":{\"enabled\":\"false\"}}]}},{\"ip-profile-ref\":\"InterVNFLink-2\",\"ip-profile-params\":{\"subnet\":[{\"name\":\"subnet-2\",\"ip-version\":\"ipv4\",\"subnet-address\":\"32.32.32.0/24\",\"dhcp-params\":{\"enabled\":\"false\"}}]}}],\"datacenter\":\"OS\",\"input-variable\":[],\"input-parameter\":[{\"xpath\":\"/nsd/vld[id=\'mgmt_vld\']/vim-network-name\",\"value\":\"private\"},{\"xpath\":\"/nsd/vld[id=\'mgmt_vld\']/ipv4-nat-pool-name\",\"value\":\"public\"},{\"xpath\":\"/nsd/vld[id=\'ping_pong_vld1\']/ip-profile-ref\",\"value\":\"InterVNFLink-1\"}],\"nsd-placement-group-maps\":[],\"vnfd-placement-group-maps\":[]},\"project-name\":\"Test1\"}}"
# print(json.loads(x))