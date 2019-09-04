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