__author__ = 'JG'

lp_addr = "10.110.5.2"

header = \
    {
        'Content-Type': "application/json",
        'Authorization': "Basic YWRtaW46YWRtaW4=",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': f"{lp_addr}:8008",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

proj_name = ""
proj_desc = ""

proj_name_default = "Autobot"
proj_desc_default = "Automation Project"

proj_user_name = "admin"
proj_user_domain = "system"
proj_role = "rw-project:project-admin"
proj_event_publish = False

cloud_acct_name = "OS"
cloud_acct_type = "OpenStack"
cloud_acct_timeout = 500

vim_os_key = "jghosh"
vim_os_secret = "mypasswd"
vim_os_auth_url = "https://keystone.es2.eng.riftio.com:5000/v3"
vim_os_user_domain = "eng"
vim_os_proj_domain = "eng"
vim_os_tenant = "jghosh"
vim_os_region = "RegionOne"
vim_os_mgmt_net = "private"
vim_os_float_ip_pool_net = "public"

ping_vnfd_ext_url = "http://10.110.0.2/descriptors/rel71/ping_vnfd.tar.gz"
pong_vnfd_ext_url = "http://10.110.0.2/descriptors/rel71/pong_vnfd.tar.gz"
ping_pong_nsd_ext_url = "http://10.110.0.2/descriptors/rel71/ping_pong_nsd.tar.gz"