__author__ = "JG"

from autobot.lib import utility as util
from autobot.lib import restAPIs as rapi
from autobot.config import payloads as pl
import time

def proj_add(lp_addr, header, proj_name, proj_desc):
    try:
        api = rapi.proj_add()
        url = util.create_url_running(lp_addr, api)
        payload = pl.proj_add(proj_name, proj_desc)

        status = util.config_add(url, header, payload)
        time.sleep(10)
        state = util.get_rpc_state(status).upper()
        return state
    except BaseException as e:
        util.log_info(e)
        raise


def proj_config(lp_addr, header, proj_name, user_name, user_domain, role, event_publish):
    try:
        api = rapi.proj_config(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = pl.proj_config(user_name, user_domain, role, event_publish)

        status = util.config_add(url, header, payload)
        time.sleep(10)
        state = util.get_rpc_state(status).upper()
        return state
    except BaseException as e:
        util.log_info(e)
        raise


def cloud_acct_add(lp_addr, header, proj_name, acct_name, acct_type, timeout):
    try:
        api = rapi.cloud_acct_add(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = pl.cloud_acct_add(acct_name, acct_type, timeout)

        status = util.config_add(url, header, payload)
        time.sleep(10)
        state = util.get_rpc_state(status).upper()
        return state
    except BaseException as e:
        util.log_info(e)
        raise


def cloud_acct_config_openstack(lp_addr, header, proj_name, cloud_acct_name, key, secret, auth_url, tenant, user_domain="eng", proj_domain="eng", region="RegionOne", mgmt_net="private", float_ip_pool_net="public"):
    try:
        api = rapi.cloud_acct_config_openstack(proj_name, cloud_acct_name)
        url = util.create_url_running(lp_addr, api)
        payload = pl.cloud_acct_config_openstack(key, secret, auth_url, user_domain, proj_domain, tenant, region, mgmt_net, float_ip_pool_net)

        status = util.config_edit(url, header, payload)
        time.sleep(10)
        state = util.get_rpc_state(status).upper()
        return state
    except BaseException as e:
        util.log_info(e)
        raise


def cloud_acct_status(lp_addr, header, proj_name, cloud_acct_name):
    try:
        api = rapi.cloud_acct_status(proj_name, cloud_acct_name)
        url = util.create_url_operational(lp_addr, api)
        payload = ""

        status = util.config_get(url, header, payload)
        time.sleep(10)
        val = list(status.values())
        return val[0]
    except BaseException as e:
        util.log_info(e)
        raise


def cloud_acct_delete(lp_addr, header, proj_name, cloud_acct_name):
    try:
        api = rapi.cloud_acct_delete(proj_name, cloud_acct_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        status = util.config_delete(url, header, payload)
        time.sleep(10)
        state = util.get_rpc_state(status).upper()
        return state
    except BaseException as e:
        util.log_info(e)
        raise


def proj_delete(lp_addr, header, proj_name):
    try:
        api = rapi.proj_delete(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        status = util.config_delete(url, header, payload)
        time.sleep(10)
        state = util.get_rpc_state(status).upper()
        return state
    except BaseException as e:
        util.log_info(e)
        raise


def pkg_onboard(lp_addr, header, proj_name, ext_url):
    try:
        api = rapi.pkg_upload()
        url = util.create_url_operations(lp_addr, api)
        payload = pl.pkg_upload(proj_name, ext_url)

        status = util.config_add(url, header, payload)
        time.sleep(10)
        transac_id = util.get_transac_id(status)
        return transac_id
    except BaseException as e:
        util.log_info(e)
        raise


def pkg_upload_status(lp_addr, header, proj_name, transac_id):
    try:
        api = rapi.pkg_upload_status(proj_name, transac_id)
        url = util.create_url_operations(lp_addr, api)
        payload = ""

        status = util.config_get(url, header, payload)
        state = list(status.values())
        print(state[0])
        return state
    except BaseException as e:
        util.log_info(e)
        raise






