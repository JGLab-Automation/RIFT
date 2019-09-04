from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.lib import restAPIs as rapi
from autobot.config import constants as const
from autobot.config import payloads as pl



# state1 = fw.proj_add(const.lp_addr, const.header, const.proj_name_default, const.proj_desc_default)
# print(state1)
#
# state2 = fw.proj_config(const.lp_addr, const.header, const.proj_name_default, const.proj_user_name,
#                         const.proj_user_domain, const.proj_role, const.proj_event_publish)
# print(state2)

# state3 = fw.cloud_acct_add(const.lp_addr, const.header, const.proj_name_default, const.cloud_acct_name,
#                            const.cloud_acct_type, const.cloud_acct_timeout)
# print(state3)
#
# state4 = fw.cloud_acct_config_openstack(const.lp_addr, const.header, const.proj_name_default, const.cloud_acct_name,
#                                         const.vim_os_key, const.vim_os_secret, const.vim_os_auth_url,
#                                         const.vim_os_tenant)
# print(state4)

status = fw.cloud_acct_status(const.lp_addr, const.header, const.proj_name, const.cloud_acct_name)
print(status)
