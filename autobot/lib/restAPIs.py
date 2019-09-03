__author__ = 'JG'

'''
Do Not add '/' at the beginning of REST URI.
Example: - rw-project:project/ and Not /rw-project:project/
'''

def project_create():
    api = "rw-project:project"
    return str(api)


def project_config(proj_name):
    pass


def project_delete(proj_name):
    api = f"rw-project:project/{proj_name}"
    return str(api)


def account_create(proj_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud"
    return api


cloud_account = '/rw-project:project/STRING/rwcal:cloud-accounts'

vnfr_catalog = 'rw-project:project/default/vnfr:vnfr-catalog/vnfr'
ns_instance_config = 'rw-project:project/default/nsr:ns-instance-config/nsr'