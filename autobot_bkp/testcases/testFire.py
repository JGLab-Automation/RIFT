from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.lib import restAPIs as rapi
from autobot.config import constants as const
from autobot.config import payloads as pl





# state1 = fw.proj_add(const.lp_addr, const.header, const.proj_name_default, const.proj_desc_default)
#
# state = fw.proj_config(const.lp_addr, const.header, const.proj_name_default, const.proj_user_name, const.proj_user_domain, const.proj_role, const.proj_event_publish)

#print(state1)
#print(state2)



state1 = fw.cloud_acct_add(const.lp_addr, const.header, const.proj_name_default, const.cloud_acct_name, const.cloud_acct_type, const.cloud_acct_timeout)
state2 = fw.cloud_acct_config(const.lp_addr, const.header, const.proj_name_default, const.cloud_acct_name, const.vim_os_key,
                              const.vim_os_secret, const.vim_os_authURL, const.vim_os_userDomain, const.vim_os_projDomain,
                              const.vim_os_tenant, const.vim_os_region, const.vim_os_mgmt_net, const.vim_os_float_ip_pool_net)
print(state1)
print(state2)
