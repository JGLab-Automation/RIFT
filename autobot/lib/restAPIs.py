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


def proj_name(proj_name):
    api = f"rw-project:project/{proj_name}/name"
    return api


def proj_config(proj_name):
    api = f"rw-project:project/{proj_name}/project-config"
    return api


def proj_user_role(proj_name):
    api = f"rw-project:project/{proj_name}/project-config/user/role"
    return api


def proj_detail(proj_name):
    api = f"rw-project:project/{proj_name}"
    return str(api)


def cloud_acct_add(proj_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account"
    return api


def cloud_acct_type(proj_name, cloud_acct_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account/{cloud_acct_name}/account-type"
    return api


def cloud_acct_config_openstack(proj_name, cloud_acct_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account/{cloud_acct_name}/openstack"
    return api


def cloud_acct_config_vcd(proj_name, cloud_acct_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account/{cloud_acct_name}/vmware-vcd"
    return api


def cloud_acct_status(proj_name, cloud_acct_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account/{cloud_acct_name}/oper-state"
    return api


def cloud_acct_detail(proj_name, cloud_acct_name):
    api = f"rw-project:project/{proj_name}/rw-cloud:cloud/account/{cloud_acct_name}"
    return api


def pkg_upload():
    api = f"package-create-update"
    return api


def pkg_upload_status(proj_name, transac_id):
    api = f"rw-project:project/{proj_name}/rw-package:package-state/package-create-update-job/{transac_id}/status"
    return api


def pkg_catalog(proj_name):
    api = f"rw-project:project/{proj_name}/rw-package:package-catalog/package"
    return api


def vnfd_catalog(proj_name):
    api = f"rw-project:project/{proj_name}/project-vnfd:vnfd-catalog/vnfd"
    return api


def vnfd_delete(proj_name, vnfd_id):
    api = f"rw-project:project/{proj_name}/project-vnfd:vnfd-catalog/vnfd/{vnfd_id}"
    return api


def nsd_catalog(proj_name):
    api = f"rw-project:project/{proj_name}/project-nsd:nsd-catalog/nsd"
    return api


def nsd_delete(proj_name, nsd_id):
    api = f"rw-project:project/{proj_name}/project-nsd:nsd-catalog/nsd/{nsd_id}"
    return api


def ns_create():
    api = "nsr:create-network-service-v2"
    return api


def ns_instance_config(proj_name, nsr_id):
    api = f"rw-project:project/{proj_name}/nsr:ns-instance-config/nsr/{nsr_id}"
    return api


def ns_instantiate():
    api = "nsr:instantiate-network-service-v2"
    return api


def ns_terminate():
    api = "nsr:terminate-network-service-v2"
    return api


def ns_delete():
    api = "nsr:delete-network-service-v2"
    return api


def ns_oper_status(proj_name, nsr_id):
    api = f"rw-project:project/{proj_name}/nsr:ns-instance-opdata/nsr/{nsr_id}/operational-status"
    return api


def vim_resource_discover():
    api = "discover-cloud-resources"
    return api