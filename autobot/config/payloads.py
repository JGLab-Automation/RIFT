__author__ = 'JG'

import json


def proj_add(proj_name, proj_desc):
    payload = \
        {
            "rw-project:project":
                {
                    "name": proj_name,
                    "description": proj_desc
                }
        }
    payload = json.dumps(payload)
    return payload


def proj_config(user_name, user_domain, role, event_publish):
    payload = \
        {
            "rw-project:project-config":
                {
                    "user":
                        [
                            {
                                "user-name": user_name,
                                "user-domain": user_domain,
                                "role":
                                    [
                                        {
                                            "role": role
                                        }
                                    ]
                            }
                        ],
                    "rw-umb-mgr:event-publish":
                        {
                            "event-publish-enable": event_publish
                        }
                }
        }
    payload = json.dumps(payload)
    return payload


def cloud_acct_add(acct_name, acct_type, timeout):
    payload = \
        {
            "rw-cloud:account":
                [
                    {
                        "name": acct_name,
                        "account-type": acct_type.lower(),
                        "vdu-instance-timeout": timeout
                    }
                ]
        }
    payload = json.dumps(payload)
    return payload


def cloud_acct_config_openstack(key, secret, auth_url, usr_domain, proj_domain, tenant, region, mgmt_net, float_ip_pool_net):
    payload = \
        {
            "key": key,
            "secret": secret,
            "auth_url": auth_url,
            "user-domain": usr_domain,
            "project-domain": proj_domain,
            "tenant": tenant,
            "region": region,
            "admin": "false",
            "mgmt-network": mgmt_net,
            "plugin-name": "rwcal_openstack",
            "dynamic-flavor-support": "true",
            "floating-ip-pool": float_ip_pool_net,
            "cert-validate": "false"
        }
    payload = json.dumps(payload)
    return payload


def cloud_acct_config_vcd(user, passwd, auth_url, tenant, mgmt_net, org, admin_user, admin_passwd, nsx_auth_url,
                          nsx_user, nsx_passwd, vc_host, vc_port, vc_user, vc_passwd):
    payload = \
        {
            "user": user,
            "password": passwd,
            "auth-url": auth_url,
            "tenant": tenant,
            "organization": org,
            "admin-credentials":
                {
                "user": admin_user,
                "password": admin_passwd
                },
            "nsx-credentials":
                {
                "auth-url": nsx_auth_url,
                "user": nsx_user,
                "password": nsx_passwd
                },
            "vcenter-credentials":
                {
                "host": vc_host,
                "port": vc_port,
                "user": vc_user,
                "password": vc_passwd
                },
            "mgmt-network": mgmt_net,
            "plugin-name": "rwcal_vmware_vcd",
            "dynamic-flavor-support": "true",
            "cert-validate": "false"
        }
    payload = json.dumps(payload)
    return payload

def pkg_upload(proj_name, ext_url):
    payload = \
        {
            "input":
                {
                    "external-url": f"{ext_url}",
                    "overwrite": "false",
                    "project-name": f"{proj_name}"
                }
        }
    payload = json.dumps(payload)
    return payload


def ns_create(proj_name, ns_name, nsd_id):
    payload = \
        {
            'input':
                {
                    'project-name': proj_name,
                    'name': ns_name,
                    'nsd-id-ref': nsd_id
                }
        }
    payload = json.dumps(payload)
    return payload


def ns_instantiate(proj_name, nsr_id):
    payload = \
        {
            'input':
                {
                    'nsr-id-ref': nsr_id,
                    'deployment-profile':
                        {
                            'config-timeout': 1200,
                            'auto-rollback': 'DISABLED',
                            'ip-profile-map':
                                [
                                    {
                                        'ip-profile-ref': 'InterVNFLink-1',
                                        'ip-profile-params':
                                            {
                                                'subnet':
                                                    [
                                                        {
                                                            'name': 'subnet-1',
                                                            'ip-version': 'ipv4',
                                                            'subnet-address': '31.31.31.0/24',
                                                            'dhcp-params':
                                                                {
                                                                    'enabled': 'false'
                                                                }
                                                        }
                                                    ]
                                            }
                                    },
                                    {
                                        'ip-profile-ref': 'InterVNFLink-2',
                                        'ip-profile-params':
                                            {
                                                'subnet':
                                                    [
                                                        {
                                                            'name': 'subnet-2',
                                                            'ip-version': 'ipv4',
                                                            'subnet-address': '32.32.32.0/24',
                                                            'dhcp-params':
                                                                {
                                                                    'enabled': 'false'
                                                                }
                                                        }
                                                    ]
                                            }
                                    }
                                ],
                            'datacenter': 'OS',
                            'input-variable': [],
                            'input-parameter':
                                [
                                    {
                                        'xpath': "/nsd/vld[id='mgmt_vld']/vim-network-name",
                                        'value': 'private'
                                    },
                                    {
                                        'xpath': "/nsd/vld[id='mgmt_vld']/ipv4-nat-pool-name",
                                        'value': 'public'
                                    },
                                    {
                                        'xpath': "/nsd/vld[id='ping_pong_vld1']/ip-profile-ref",
                                        'value': 'InterVNFLink-1'
                                    }
                                ],
                            'nsd-placement-group-maps': [],
                            'vnfd-placement-group-maps': []
                        },
                    'project-name': proj_name
                }
        }
    payload = json.dumps(payload)
    return payload


def ns_terminate(proj_name, nsr_id):
    payload = \
        {
            'input':
                {
                    'project-name': proj_name,
                    'nsr-id-ref': nsr_id
                }
        }
    payload = json.dumps(payload)
    return payload


def ns_delete(proj_name, nsr_id):
    payload = \
        {
            'input':
                {
                    'project-name': proj_name,
                    'nsr-id-ref': nsr_id
                }
        }
    payload = json.dumps(payload)
    return payload


def vim_resource_discover(proj_name, cloud_acct_name):
    payload = \
        {
            'input':
                {
                    'cloud-account': cloud_acct_name,
                    'project-name': proj_name
                }
        }
    payload = json.dumps(payload)
    return payload


def input_parameter_xpath_nsd(xpath, default_value):
    payload = \
        {
            "project-nsd:input-parameter-xpath":
                [
                    {
                        "xpath": f"{xpath}",
                        "default-value": f"{default_value}"
                    }
                ]
        }
    payload = json.dumps(payload)
    return payload

def input_parameter_xpath_nsr(xpath, default_value):
    payload = \
        {
            "nsr:input-parameter-xpath":
                [
                    {
                        "xpath": f"{xpath}",
                        "default-value": f"{default_value}"
                    }
                ]
        }
    payload = json.dumps(payload)
    return payload

