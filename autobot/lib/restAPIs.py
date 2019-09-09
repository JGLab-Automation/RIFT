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


def cloud_acct_config_openstack(proj_name, cloud_acct_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account/{cloud_acct_name}/openstack"
    return api


def cloud_acct_status(proj_name, cloud_acct_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account/{cloud_acct_name}/oper-state/status"
    return api


def cloud_acct_delete(proj_name, cloud_acct_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account/{cloud_acct_name}"
    return api


def pkg_upload():
    api = f"package-create-update"
    return api


def pkg_upload_status(proj_name, transac_id):
    api = f"rw-project:project/{proj_name}/rw-package:package-state/package-create-update-job/{transac_id}/status"
    return api


