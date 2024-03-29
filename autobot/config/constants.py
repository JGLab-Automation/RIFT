__author__ = 'JG'

lp_addr = ["10.110.5.1"]
lp_addr_web = f"http://{lp_addr[0]}"

header = \
    {
        'Content-Type': "application/json",
        'Authorization': "Basic YWRtaW46YWRtaW4=",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': f"{lp_addr[0]}:8008",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

lp_addr_default = ["10.110.5.0", "10.68.102.219", "10.68.102.228"]
header_default = \
    {
        'Content-Type': "application/json",
        'Authorization': "Basic YWRtaW46YWRtaW4=",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': f"{lp_addr_default[0]}:8008",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
web_addr_default = f"http://{lp_addr_default[0]}"

proj_name_default = "Autobot"
proj_desc_default = "Automation Project"

proj_user_name = "admin"
proj_user_domain = "system"
proj_role = "rw-project:project-admin"
proj_event_publish = False


cloud_acct_name = ["OS", "Autobot_VCD"]
cloud_acct_type = ["OpenStack", "VMWare-VCD"]
cloud_acct_timeout = [300, 1000]

vim_os_key = "jghosh"
vim_os_secret = "mypasswd"
vim_os_auth_url = "https://keystone.es2.eng.riftio.com:5000/v3"
vim_os_user_domain = "eng"
vim_os_proj_domain = "eng"
vim_os_tenant = "jghosh_automation"
vim_os_region = "RegionOne"
vim_os_mgmt_net = "private"
vim_os_float_ip_pool_net = "public"

vim_vcd91_user = "hash123"
vim_vcd91_passwd = "hash123"
vim_vcd91_auth_url = "https://10.66.0.200"
vim_vcd91_tenant = "ENG-VDC1"
vim_vcd91_mgmt_net = "mgmt_network-d39198f9-2e35-4779-b200-b06215cc0f2a"
vim_vcd91_org = "ENG"
vim_vcd91_admin_user = "administrator"
vim_vcd91_admin_passwd = "riftIO18"
vim_vcd91_nsx_auth_url = "https://10.66.0.228"
vim_vcd91_nsx_user = "admin"
vim_vcd91_nsx_passwd = "riftIO18!"
vim_vcd91_vc_host = "10.66.0.221"
vim_vcd91_vc_port = "443"
vim_vcd91_vc_user = "administrator@vsphere.local"
vim_vcd91_vc_passwd = "riftIO18!"


running_dir = []

release = ["rel72"]
ping_vnfd_ext_url = f"http://10.110.0.2/descriptors/{release[0]}/ping_vnfd.tar.gz"
pong_vnfd_ext_url = f"http://10.110.0.2/descriptors/{release[0]}/pong_vnfd.tar.gz"
ping_pong_nsd_ext_url = f"http://10.110.0.2/descriptors/{release[0]}/ping_pong_nsd.tar.gz"

"""
#-----------------------------------------------------------------------------------------------------------------------
Constants for WebUI support.
#-----------------------------------------------------------------------------------------------------------------------
"""

browser_type = "Chrome"
scr_shot = "./artifacts/screenshots/"