__author__ = 'JG'

'''
Do Not add '/' at the beginning & end of REST URI.
Example: -
Correct:    rw-project:project
Wrong:      /rw-project:project/
'''

def proj_add():
    api = "rw-project:project"
    return str(api)


def proj_config(proj_name):
    api = f"rw-project:project/{proj_name}/project-config"
    return api


def proj_delete(proj_name):
    api = f"rw-project:project/{proj_name}"
    return str(api)


def cloud_acct_add(proj_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account"
    return api


def cloud_acct_config(proj_name, cloud_acct_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account/{cloud_acct_name}"
    return api


def cloud_acct_config_openstack(proj_name, cloud_acct_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account/{cloud_acct_name}/openstack"
    return api


cloud_account = 'rw-project:project/STRING/rwcal:cloud-accounts'

vnfr_catalog = 'rw-project:project/default/vnfr:vnfr-catalog/vnfr'
ns_instance_config = 'rw-project:project/default/nsr:ns-instance-config/nsr'