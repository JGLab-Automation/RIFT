__author__ = "JG"

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
import sys
import inspect
from datetime import datetime

from autobot.lib import utility as util
from autobot.lib import restAPIs as rapi
from autobot.config import payloads as pl
from autobot.config import constants as const

def get_lp_version(lp_addr, header):
    try:
        api = rapi.lp_version()
        url = util.create_url_operational(lp_addr, api)
        payload = ""

        util.log_info("Fetching build-version of the LP.")
        version = util.get_config(url, header, payload)
        lp_version = version["rw-base:version"]["version"]
        time.sleep(5)
        return lp_version
    except BaseException as e:
        util.log_info(e)
        raise


def proj_add(lp_addr, header, proj_name, proj_desc):
    try:
        api = rapi.proj_add()
        url = util.create_url_running(lp_addr, api)
        payload = pl.proj_add(proj_name, proj_desc)

        util.log_info(f"Adding project with name- {proj_name}.")
        status = util.add_config(url, header, payload)
        state = util.get_rpc_state(status).upper()
        if state != "OK":
            assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
        time.sleep(15)
    except BaseException as e:
        util.log_info(e)
        raise


def get_proj_name(lp_addr, header, proj_name):
    try:
        api = rapi.proj_name(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info("Fetching project name.")
        status = util.get_config(url, header, payload)
        time.sleep(5)
        return status["name"]
    except BaseException as e:
        util.log_info(e)
        raise


def proj_config(lp_addr, header, proj_name, user_name, user_domain, role, event_publish):
    try:
        api = rapi.proj_config(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = pl.proj_config(user_name, user_domain, role, event_publish)

        util.log_info(f"Configuring project- {proj_name}.")
        status = util.add_config(url, header, payload)
        state = util.get_rpc_state(status).upper()
        if state != "OK":
            assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
        time.sleep(20)
    except BaseException as e:
        util.log_info(e)
        raise


def get_proj_user_role(lp_addr, header, proj_name):
    try:
        api = rapi.proj_user_role(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching user-role for project- {proj_name}.")
        status = util.get_config(url, header, payload)
        time.sleep(10)
        role = status["rw-project:user"]["role"][0]
        return role
    except BaseException as e:
        util.log_info(e)
        raise


def proj_delete(lp_addr, header, proj_name):
    try:
        api = rapi.proj_detail(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Deleting project with name- {proj_name}.")
        status = util.delete_config(url, header, payload)
        time.sleep(10)
        state = util.get_rpc_state(status).upper()
        if state != "OK":
            assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
    except BaseException as e:
        util.log_info(e)
        raise


def get_proj_details(lp_addr, header, proj_name):
    try:
        api = rapi.proj_detail(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching project details for project- {proj_name}.")
        status = util.get_config(url, header, payload)
        time.sleep(5)
        return status
    except BaseException as e:
        util.log_info(e)
        raise


def cloud_acct_add(lp_addr, header, proj_name, acct_name, acct_type, timeout):
    try:
        api = rapi.cloud_acct_add(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = pl.cloud_acct_add(acct_name, acct_type, timeout)

        util.log_info(f"Adding cloud account- {acct_type} with name- {acct_name} to project- {proj_name}.")
        status = util.add_config(url, header, payload)
        time.sleep(10)
        state = util.get_rpc_state(status).upper()
        if state != "OK":
            assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
    except BaseException as e:
        util.log_info(e)
        raise


def get_cloud_acct_details(lp_addr, header, proj_name, cloud_acct_name):
    try:
        api = rapi.cloud_acct_detail(proj_name, cloud_acct_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching cloud-account details for account with name- {cloud_acct_name}.")
        status = util.get_config(url, header, payload)
        time.sleep(5)
        return status
    except BaseException as e:
        util.log_info(e)
        raise


def get_cloud_acct_type(lp_addr, header, proj_name, acct_name):
    try:
        api = rapi.cloud_acct_type(proj_name, acct_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching account-type for cloud-account- {acct_name}.")
        status = util.get_config(url, header, payload)
        time.sleep(5)
        return status["account-type"]
    except BaseException as e:
        util.log_info(e)
        raise


def cloud_acct_config_openstack(lp_addr, header, proj_name, cloud_acct_name, key, secret, auth_url, tenant,
                                user_domain="eng", proj_domain="eng", region="RegionOne", mgmt_net="private",
                                float_ip_pool_net="public"):
    try:
        api = rapi.cloud_acct_config_openstack(proj_name, cloud_acct_name)
        url = util.create_url_running(lp_addr, api)
        payload = pl.cloud_acct_config_openstack(key, secret, auth_url, user_domain, proj_domain, tenant, region,
                                                 mgmt_net, float_ip_pool_net)

        util.log_info(f"Adding configuration to cloud-account- {cloud_acct_name}.")
        status = util.edit_config(url, header, payload)
        time.sleep(20)
        state = util.get_rpc_state(status).upper()
        if state != "OK":
            assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
    except BaseException as e:
        util.log_info(e)
        raise


def cloud_acct_config_vcd(lp_addr, header, proj_name, cloud_acct_name, user, passwd, auth_url, tenant, mgmt_net, org,
                          admin_user, admin_passwd, nsx_auth_url, nsx_user, nsx_passwd,
                          vc_host, vc_port, vc_user, vc_passwd):
    try:
        api = rapi.cloud_acct_config_vcd(proj_name, cloud_acct_name)
        url = util.create_url_running(lp_addr, api)
        payload = pl.cloud_acct_config_vcd(user, passwd, auth_url, tenant, mgmt_net, org, admin_user, admin_passwd,
                                           nsx_auth_url, nsx_user, nsx_passwd, vc_host, vc_port, vc_user, vc_passwd)
        util.log_info(f"Adding configuration to cloud-account- {cloud_acct_name}.")
        status = util.edit_config(url, header, payload)
        time.sleep(20)
        state = util.get_rpc_state(status).upper()
        if state != "OK":
            assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
    except BaseException as e:
        util.log_info(e)
        raise


def cloud_acct_status(lp_addr, header, proj_name, cloud_acct_name):
    try:
        api = rapi.cloud_acct_status(proj_name, cloud_acct_name)
        url = util.create_url_operational(lp_addr, api)
        payload = ""

        status = util.get_config(url, header, payload)
        time.sleep(10)
        return status["rw-cloud:oper-state"]["status"]

        #state = list(status.values())
        #return state[0]
    except BaseException as e:
        util.log_info(e)
        raise


def cloud_acct_delete(lp_addr, header, proj_name, cloud_acct_name):
    try:
        api = rapi.cloud_acct_detail(proj_name, cloud_acct_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        status = util.delete_config(url, header, payload)
        time.sleep(15)
        state = util.get_rpc_state(status).upper()
        if state != "OK":
            assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
    except BaseException as e:
        util.log_info(e)
        raise


def pkg_onboard(lp_addr, header, proj_name, ext_url):
    try:
        api = rapi.pkg_upload()
        url = util.create_url_operations(lp_addr, api)
        payload = pl.pkg_upload(proj_name, ext_url)

        util.log_info(f"Adding package to project- {proj_name}.")
        status = util.add_config(url, header, payload)
        transac_id = util.get_transac_id(status)
        if transac_id:
            util.log_info(f"TransactionID for uploaded package- {transac_id}.")
            time.sleep(20)
            return transac_id
        else:
            assert transac_id, "Expecting transaction-ID when package is uploaded."
    except BaseException as e:
        util.log_info(e)
        raise


def pkg_upload_status(lp_addr, header, proj_name, transac_id):
    try:
        api = rapi.pkg_upload_status(proj_name, transac_id)
        url = util.create_url_operations(lp_addr, api)
        payload = ""

        util.log_info(f"Checking status of uploaded package in project- {proj_name}.")
        status = util.get_config(url, header, payload)
        state = list(status.values())
        util.log_info(f"Package upload status- {state[0]}.")
        time.sleep(5)
        return state[0]
    except BaseException as e:
        util.log_info(e)
        raise


def get_vnfd_id(lp_addr, header, proj_name):
    try:
        vnfd_id = []

        api = rapi.vnfd_catalog(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching VNFD ID(s) from project- {proj_name}.")
        status = util.get_config(url, header, payload)
        vnfd_catalog = status['project-vnfd:vnfd']
        for i in range(0, len(vnfd_catalog)):
            vnfd_id.append(vnfd_catalog[i]['id'])
        time.sleep(5)
        return vnfd_id
    except BaseException as e:
        util.log_info(e)
        raise


def get_vnfd_name(lp_addr, header, proj_name):
    try:
        vnfd_name = []

        api = rapi.vnfd_catalog(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching VNFD name(s) from project- {proj_name}.")
        status = util.get_config(url, header, payload)
        vnfd_catalog = status['project-vnfd:vnfd']
        for i in range(len(vnfd_catalog)):
            vnfd_name.append(vnfd_catalog[i]['name'])
        time.sleep(5)
        return vnfd_name
    except BaseException as e:
        util.log_info(e)
        raise


def get_nsd_id(lp_addr, header, proj_name):
    try:
        nsd_id = []

        api = rapi.nsd_catalog(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching NSD-ID(s) from project- {proj_name}.")
        status = util.get_config(url, header, payload)
        if status is not None:
            nsd_catalog = status['project-nsd:nsd']
            for i in range(0, len(nsd_catalog)):
                nsd_id.append(nsd_catalog[i]['id'])
            return nsd_id
        else:
            util.log_info("NSD package(s) not available.")
    except BaseException as e:
        util.log_info(e)
        raise


def get_nsd_name(lp_addr, header, proj_name):
    try:
        nsd_name = []

        api = rapi.nsd_catalog(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching NSD name(s) from project- {proj_name}.")
        status = util.get_config(url, header, payload)
        if status is not None:
            nsd_catalog = status['project-nsd:nsd']
            for i in range(len(nsd_catalog)):
                nsd_name.append(nsd_catalog[i]['name'])
            return nsd_name
        else:
            util.log_info("NSD package(s) not available.")
    except BaseException as e:
        util.log_info(e)
        raise


def get_nsd_name_id(lp_addr, header, proj_name):
    try:
        nsd_id = get_nsd_id(lp_addr, header, proj_name)
        nsd_name = get_nsd_name(lp_addr, header, proj_name)
        if nsd_id and nsd_name:
            nsd = dict(zip(nsd_name, nsd_id))
            util.log_info(f"Available NSD(s)- {list(nsd.keys())}.")
            return nsd
        else:
            util.log_info("NSD ID & Name couldn't map.")
    except BaseException as e:
        util.log_info(e)
        raise


def get_vnfr_id(lp_addr, header, proj_name):
    try:
        vnfr_id = []

        api = rapi.vnfr_catalog(proj_name)
        url = util.create_url_operational(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching VNFR details.")
        status = util.get_config(url, header, payload)
        if status is not None:
            vnfr_catalog = status["vnfr:vnfr"]
            for items in vnfr_catalog:
                vnfr_id.append(items["id"])
            return vnfr_id
        else:
            assert status, "VNFR details not available."
    except BaseException as e:
        util.log_info(e)
        raise


def get_vnfr_name(lp_addr, header, proj_name):
    try:
        vnfr_id = []

        api = rapi.vnfr_catalog(proj_name)
        url = util.create_url_operational(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching VNFR details.")
        status = util.get_config(url, header, payload)
        if status is not None:
            vnfr_catalog = status["vnfr:vnfr"]
            for items in vnfr_catalog:
                vnfr_id.append(items["short-name"])
            return vnfr_id
        else:
            assert status, "VNFR details not available."
    except BaseException as e:
        util.log_info(e)
        raise


def get_vdur_vim_id(lp_addr, header, proj_name, vnfr_id):
    try:
        vdur_vim_id = []

        api = rapi.vdur_detail(proj_name, vnfr_id)
        url = util.create_url_operational(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching VDUR details.")
        status = util.get_config(url, header, payload)
        if status is not None:
            vdur_catalog = status["vnfr:vdur"]
            for items in vdur_catalog:
                vdur_vim_id.append(items["vim-id"])
            return vdur_vim_id
        else:
            assert status, "VDUR details not available."
    except BaseException as e:
        util.log_info(e)
        raise


def get_vdu_name_id(lp_addr, header, proj_name):
    try:
        vdur_vim_id = []
        util.log_info("Mapping VDUR VIM-ID with VNFR-Name.")
        vnfr_ids = get_vnfr_id(lp_addr, header, proj_name)
        for ids in vnfr_ids:
            vdu_vim_ids = get_vdur_vim_id(lp_addr, header, proj_name, ids)
            for ids in vdu_vim_ids:
                vdur_vim_id.append(ids)
        vnfr_name = get_vnfd_name(lp_addr, header, proj_name)
        if vdur_vim_id and vnfr_name:
            vdu = dict(zip(vnfr_name, vdur_vim_id))
            util.log_info(f"Available VDUR(s)- {list(vdu.keys())}.")
            return vdu
        else:
            util.log_info("VDUR VIM-ID & VNFR-Name couldn't map.")
    except BaseException as e:
        util.log_info(e)
        raise


def pkg_delete(lp_addr, header, proj_name, pkg_type, pkg_name):
    try:
        vnfd = {}
        nsd = {}
        pkg = {}
        util.log_info("Collecting VNFD ID.")
        vnfd_id = get_vnfd_id(lp_addr, header, proj_name)
        util.log_info("Collecting VNFD Name.")
        vnfd_name = get_vnfd_name(lp_addr, header, proj_name)
        util.log_info("Collecting NSD ID.")
        nsd_id = get_nsd_id(lp_addr, header, proj_name)
        util.log_info("Collecting NSD Name.")
        nsd_name = get_nsd_name(lp_addr, header, proj_name)

        if vnfd_id and vnfd_name:
            vnfd = dict(zip(vnfd_name, vnfd_id))
        if nsd_id and nsd_name:
            nsd = dict(zip(nsd_name, nsd_id))
        if bool(vnfd) or bool(nsd):
            pkg = {**vnfd, **nsd}
            util.log_info(f"Available packages: {pkg}.")

        if pkg_type.upper() == "VNFD":
            api = rapi.vnfd_delete(proj_name, pkg[pkg_name])
            url = util.create_url_running(lp_addr, api)
            payload = ""
            util.log_info(f"Deleting package: {pkg_name} with ID: {pkg[pkg_name]}")
            status = util.delete_config(url, header, payload)
            time.sleep(20)
            state = util.get_rpc_state(status).upper()
            if state != "OK":
                assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
        elif pkg_type.upper() == "NSD":
            api = rapi.nsd_delete(proj_name, pkg[pkg_name])
            url = util.create_url_running(lp_addr, api)
            payload = ""
            util.log_info(f"Deleting package: {pkg_name} with ID: {pkg[pkg_name]}")
            status = util.delete_config(url, header, payload)
            time.sleep(20)
            state = util.get_rpc_state(status).upper()
            if state != "OK":
                assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
    except BaseException as e:
        util.log_info(e)
        raise


def get_pkg_catalog(lp_addr, header, proj_name, value=None):
    try:
        prod_name = []

        api = rapi.pkg_catalog(proj_name)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        status = util.get_config(url, header, payload)
        if status:
            pkgs = (list(status.values())[0])
            if value is None:
                return pkgs
            elif value == "name":
                for pkg in pkgs:
                    prod_name.append(pkg["product-name"])
                return prod_name
        else:
            return None
            #assert status, f"Packages not available."
    except BaseException as e:
        util.log_info(e)
        raise


def ns_create(lp_addr, header, proj_name, ns_name, nsd_id):
    try:
        api = rapi.ns_create()
        url = util.create_url_operations(lp_addr, api)
        payload = pl.ns_create(proj_name, ns_name, nsd_id)

        util.log_info(f"Creating NS with name- {ns_name} and NSD ID- {nsd_id}.")
        status = util.add_config(url, header, payload)
        nsr_id = util.get_nsr_id(status)
        util.log_info(f"Generated NSR ID- {nsr_id}.")
        time.sleep(20)
        return nsr_id
        #transac_state = util.get_transac_id(status)
        #return nsr_id, transac_state
    except BaseException as e:
        util.log_info(e)
        raise


def ns_instantiate(lp_addr, header, proj_name, nsr_id):
    try:
        api = rapi.ns_instantiate()
        url = util.create_url_operations(lp_addr, api)
        payload = pl.ns_instantiate(proj_name, nsr_id)

        util.log_info(f"Instantiating NS with NSR ID- {nsr_id}.")
        status = util.add_config(url, header, payload)
        util.log_info("Please wait while for a few minutes while instantiation is in progress.")
        time.sleep(360)
        # state = util.get_transac_id(status)
        # return state
    except BaseException as e:
        util.log_info(e)
        raise


def ns_terminate(lp_addr, header, proj_name, nsr_id):
    try:
        api = rapi.ns_terminate()
        url = util.create_url_operations(lp_addr, api)
        payload = pl.ns_terminate(proj_name, nsr_id)

        util.log_info(f"Terminating NS with NSR ID- {nsr_id}.")
        status = util.add_config(url, header, payload)
        util.log_info(f"Please wait while terminating NS.")
        # state = util.get_transac_id(status)
        time.sleep(120)
        # return state
    except BaseException as e:
        util.log_info(e)
        raise


def ns_delete(lp_addr, header, proj_name, nsr_id):
    try:
        api = rapi.ns_delete()
        url = util.create_url_operations(lp_addr, api)
        payload = pl.ns_delete(proj_name, nsr_id)

        util.log_info(f"Deleting NS with NSR ID- {nsr_id}.")
        status = util.add_config(url, header, payload)
        util.log_info(f"Please wait while deleting NS.")
        #state = util.get_transac_id(status)
        time.sleep(15)
        #return state
    except BaseException as e:
        util.log_info(e)
        raise


def get_ns_oper_status(lp_addr, header, proj_name, nsr_id):
    try:
        api = rapi.ns_oper_status(proj_name, nsr_id)
        url = util.create_url_operations(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching operational-status of NS with NSR ID: {nsr_id}.")
        status = util.get_config(url, header, payload)
        state = status["operational-status"]
        util.log_info(f"Current state of NS is- {state}.")
        time.sleep(5)
        return state
    except BaseException as e:
        util.log_info(e)
        raise


def get_ns_instance_config(lp_addr, header, proj_name, nsr_id, value=None):
    try:
        api = rapi.ns_instance_config(proj_name, nsr_id)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching NS config for NSR ID: {nsr_id}.")
        ns_config = util.get_config(url, header, payload)
        config = list(ns_config.values())
        if value is None:
            util.log_info(f"Checking NS config.")
            time.sleep(5)
            util.log_info(f"NS instance name- {config}.")
        elif value.lower() == "name":
            util.log_info(f"Fetching NS name.")
            time.sleep(5)
            util.log_info(f"NS instance name- {config[0]['name']}.")
            return config[0]["name"]
        elif value.lower() == "status":
            util.log_info(f"Fetching NS admin status.")
            time.sleep(5)
            util.log_info(f"NS instance status- {config[0]['admin-status']}.")
            return config[0]["admin-status"]
        elif value.lower() == "rollback":
            util.log_info(f"Fetching NS rollback status.")
            time.sleep(5)
            util.log_info(f"NS instance status- {config[0]['auto-rollback']}.")
            return config[0]["auto-rollback"]
        elif value.lower() == "timeout":
            util.log_info(f"Fetching NS timeout.")
            time.sleep(5)
            util.log_info(f"NS instance status- {config[0]['config-timeout']}.")
            return config[0]["config-timeout"]
    except BaseException as e:
        util.log_info(e)
        raise


def vim_resource_discover(lp_addr, header, proj_name, cloud_acct_name):
    try:
        api = rapi.vim_resource_discover()
        url = util.create_url_operations(lp_addr, api)
        payload = pl.vim_resource_discover(proj_name, cloud_acct_name)

        util.log_info(f"Discovering resources for VIM account- {cloud_acct_name}.")
        status = util.add_config(url, header, payload)
        util.log_info("Please wait while resource-discovery is in progress.")
        state = util.get_rpc_state(status).upper()
        if state != "OK":
            assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
        time.sleep(120)
    except BaseException as e:
        util.log_info(e)
        raise


def vim_discover_status(lp_addr, header, proj_name, cloud_acct_name):
    try:
        api = rapi.cloud_acct_status(proj_name, cloud_acct_name)
        url = util.create_url_operational(lp_addr, api)
        payload = ""

        status = util.get_config(url, header, payload)
        time.sleep(5)
        return status["rw-cloud:oper-state"]["disc-status"]
    except BaseException as e:
        util.log_info(e)
        raise


def vim_discovered_details(lp_addr, header, proj_name, cloud_acct_name):
    try:
        api = rapi.cloud_acct_status(proj_name, cloud_acct_name)
        url = util.create_url_operational(lp_addr, api)
        payload = ""

        status = util.get_config(url, header, payload)
        time.sleep(5)
        return status["rw-cloud:oper-state"]
    except BaseException as e:
        util.log_info(e)
        raise


def add_input_param_xpath_nsd(lp_addr, header, proj_name, nsd_id, xpath, value):
    try:
        api = rapi.input_parameter_xpath_nsd(proj_name, nsd_id)
        url = util.create_url_running(lp_addr, api)
        payload = pl.input_parameter_xpath_nsd(xpath, value)

        util.log_info(f"Adding xPath- \"{xpath}\" with value- \"{value}\" to NSD- \"{nsd_id}\".")
        status = util.add_config(url, header, payload)
        time.sleep(10)
        state = util.get_rpc_state(status).upper()
        if state != "OK":
            assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
    except BaseException as e:
        util.log_info(e)
        raise


def get_input_param_xpath_nsd(lp_addr, header, proj_name, nsd_id):
    try:
        api = rapi.input_parameter_xpath_nsd(proj_name, nsd_id)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching xPaths from NSD- {nsd_id}.")
        status = util.get_config(url, header, payload)
        return status["project-nsd:input-parameter-xpath"]
    except BaseException as e:
        util.log_info(e)
        raise


def add_input_param_xpath_nsr(lp_addr, header, proj_name, nsr_id, xpath, value):
    try:
        api = rapi.input_parameter_xpath_nsr(proj_name, nsr_id)
        url = util.create_url_running(lp_addr, api)
        payload = pl.input_parameter_xpath_nsd(xpath, value)

        util.log_info(f"Adding xPath- \"{xpath}\" with value- \"{value}\" to NSR ID- \"{nsr_id}\".")
        status = util.add_config(url, header, payload)
        time.sleep(10)
        state = util.get_rpc_state(status).upper()
        if state != "OK":
            assert state == "OK", f"RPC response: Expected - OK, Received- {state}."
    except BaseException as e:
        util.log_info(e)
        raise


def get_input_param_xpath_nsr(lp_addr, header, proj_name, nsr_id):
    try:
        api = rapi.input_parameter_xpath_nsd(proj_name, nsr_id)
        url = util.create_url_running(lp_addr, api)
        payload = ""

        util.log_info(f"Fetching xPaths from NSD- {nsr_id}.")
        status = util.get_config(url, header, payload)
        return status["nsr:input-parameter-xpath"]
    except BaseException as e:
        util.log_info(e)
        raise






"""
#-----------------------------------------------------------------------------------------------------------------------
Framework for WebUI support.
#-----------------------------------------------------------------------------------------------------------------------
"""


class BrowserTests(object):

    @classmethod
    def setup_browser(cls):
        if const.browser_type.lower() == 'firefox':
            #cls.browser = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.FIREFOX)
            cls.browser = webdriver.Firefox()
            cls.browser.maximize_window()
        elif const.browser_type.lower() == 'ie':
            cls.browser = webdriver.Ie()
        elif const.browser_type.lower() == 'chrome':
            #driver = webdriver.Chrome("/Library/Python/2.7/site-packages/selenium/webdriver/chrome/chromedriver")
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument("--start-maximized")
            cls.browser = webdriver.Chrome(chrome_options=options)
#            cls.browser = webdriver.Chrome()
            cls.browser.maximize_window()
        elif const.browser_type.lower() == 'safari':
            cls.browser = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.SAFARI)
        else:
            cls.browser = ''
            sys.exit(f"Unrecognized browser {const.browser_type}.")
        #go_to_url(cls.browser, const.BASE_URL)
        if const.browser_type.lower() == 'ie':
            cls.browser.get('javascript:document.getElementById("overridelink").click();')
        # if not os.path.exists(const.REPORT_PATH):
        #     os.mkdir(const.REPORT_PATH)
        # if os.path.exists(const.scr_shot):
        #     os.popen('rm -rf '+const.scr_shot)
        # os.mkdir(const.scr_shot)


def go_to_url(browser, url):
    util.log_info(f"Navigating to- {url}.")
    browser.get(url)
    wait_for_ajax_to_complete(browser)
    time.sleep(1)


def click_by_id(browser, id_):
    try:
        find_element_by_id(browser, id_).click()
    except BaseException:
        capture_screenshot(browser)
        raise


def click_by_xpath(browser, xpath):
    try:
        find_element_by_xpath(browser, xpath).click()
    except BaseException:
        capture_screenshot(browser)
        raise


def click_by_class_name(browser, class_name):
    try:
        find_element_by_class_name(browser, class_name).click()
    except BaseException:
        capture_screenshot(browser)
        raise


def input_by_id(browser, id_, value):
    try:
        find_element_by_id(browser, id_).send_keys(value)
    except BaseException:
        capture_screenshot(browser)
        raise


def input_by_xpath(browser, xpath, value):
    try:
        find_element_by_xpath(browser, xpath).send_keys(value)
    except BaseException:
        capture_screenshot(browser)
        raise


def input_by_class_name(browser, class_name, value):
    try:
        find_element_by_class_name(browser, class_name).send_keys(value)
    except BaseException:
        capture_screenshot(browser)
        raise


def find_element_by_id(browser, id_):
    try:
        return browser.find_element_by_id(id_)
    except BaseException:
        capture_screenshot(browser)
        raise


def find_element_by_xpath(browser, xpath):
    try:
        return browser.find_element_by_xpath(xpath)
    except BaseException:
        capture_screenshot(browser)
        raise


def find_element_by_class_name(browser, class_name):
    try:
        return browser.find_element_by_class_name(class_name)
    except BaseException:
        capture_screenshot(browser)
        raise


def find_elements_by_id(browser, id_):
    try:
        return browser.find_elements_by_id(id_)
    except BaseException:
        capture_screenshot(browser)
        raise


def find_elements_by_xpath(browser, xpath):
    try:
        return browser.find_elements_by_xpath(xpath)
    except BaseException:
        capture_screenshot(browser)
        raise


def get_element_by_id(browser, id_):
    try:
        wait_for_ajax_to_complete(browser)
        return find_element_by_id(browser, id_).text
    except BaseException:
        capture_screenshot(browser)
        raise


def find_elements_by_class_name(browser, class_name):
    try:
        return browser.find_elements_by_class_name(class_name)
    except BaseException:
        capture_screenshot(browser)
        raise


def capture_screenshot(browser,file_name=None):
    if not file_name:
        browser.get_screenshot_as_file(const.scr_shot+inspect.stack()[3][3] + '_' + inspect.stack()[2][3]
                                       + '_' + inspect.stack()[1][3] + '.png')
        print('<a href="' + '../' + const.scr_shot + inspect.stack()[3][3] + '_'+inspect.stack()[2][3] + '_' + \
              inspect.stack()[1][3] + '.png' + '">Screenshot</a>')
    else:
        browser.get_screenshot_as_file(const.scr_shot + file_name + '.png')
        print('<a href="' + '../' + const.scr_shot + file_name + '.png' + '">Screenshot</a>')


def get_links(browser):
    #return browser.find_elements_by_tag_name('a')
    links = []
    for element in browser.find_elements_by_xpath('//a'):
        links.append(element.get_attribute('href'))
    return links


def scroll_to(browser, x, y):
    browser.execute_script("window.scrollTo("+str(x)+","+str(y)+")")


def assert_true(actual, expected, message):
    try:
        assert actual == expected, message
    except AssertionError as e:
        util.log_info(e)
        raise
    return True


def assert_false(actual, expected, message):
    try:
        assert not actual == expected, message
    except AssertionError as e:
        util.log_info(e)
        raise
    return True


def start_time():
    try:
        return datetime.now()
    except BaseException:
        raise


def run_time(start_time):
    try:
        run_time = datetime.now() - start_time
        return run_time
    except BaseException:
        raise


def explicit_wait(browser, xpath, wait=60, arg='presence'):
    if arg == 'presence':
        WebDriverWait(browser, wait).until(EC.presence_of_element_located((By.XPATH, xpath)))
    if arg == 'visibility':
        WebDriverWait(browser, wait).until(EC.visibility_of_element_located((By.XPATH, xpath)))


def implicit_wait(browser, wait=60):
    browser.implicitly_wait(wait)


def get_attribute_by_xpath(browser, xpath, value):
    wait_for_ajax_to_complete(browser)
    return find_element_by_xpath(browser, xpath).get_attribute(value)


def get_text_by_xpath(browser, xpath):
    try:
        wait_for_ajax_to_complete(browser)
        return browser.find_element_by_xpath(xpath).text
    except BaseException:
        raise


def set_attribute_by_xpath(browser, xpath, value):
    try:
        output = browser.find_element_by_xpath(xpath)
        output.value = value
    except BaseException:
        raise


def send_key_strokes(browser, xpath, value):
    try:
        browser.find_element_by_xpath(xpath).clear()
        browser.find_element_by_xpath(xpath).send_keys(value)
    except BaseException:
        raise


def clear(browser, xpath):
    try:
        browser.find_element_by_xpath(xpath).clear()
    except BaseException:
        raise


def maximize(browser):
    try:
        util.log_info("Maximizing Window")
        browser.maximize_window()
    except BaseException:
        raise


def accept_alert(browser):
    try:
        util.log_info("Accepting Alert")
        browser.switch_to_alert().accept()
    except BaseException:
        raise


def dismiss_alert(browser):
    try:
        util.log_info("Dismissing Alert")
        browser.switch_to_alert().dismiss()
    except BaseException:
        raise


def checkbox_is_selected(browser, xpath):
    return find_element_by_xpath(browser, xpath).is_selected()


def checkbox_is_selected_old(browser, xpath):
    return browser.find_element_by_xpath(xpath).is_selected()


def refresh(browser):
    try:
        browser.refresh()
        time.sleep(2)
    except BaseException:
        raise


def close(browser):
    try:
        browser.close()
    except BaseException:
        raise


def clear_field(browser, xpath):
    """
        return successful if clear
    """
    for c in range(120):
        find_element_by_xpath(browser, xpath).clear()
        if find_element_by_xpath(browser, xpath).get_attribute('value') == '':
            return True
    capture_screenshot(browser)
    raise Exception("Input field is not cleared {elem}".format(elem=xpath))


def clear_field_id(browser, id):
    """
        return successful if clear
    """
    for c in range(120):
        find_element_by_id(browser, id).clear()
        if find_element_by_id(browser, id).get_attribute('value') == '':
            return True

    capture_screenshot(browser)
    raise Exception("Input field is not cleared {elem}".format(elem=id))


def write_text(browser, xpath, value):
    """
        Ensure text box is clear then write
    """
    if clear_field(browser, xpath):
        find_element_by_xpath(browser, xpath).send_keys(str(value))


def click_button(browser, xpath):
    """
        Click button by sending ENTER key
    """
    find_element_by_xpath(browser, xpath).send_keys(Keys.ENTER)


def wait_for_ajax_to_complete(browser):
    """
        Wait for Ajax by checking jQuery activation
    """
    wait = WebDriverWait(browser, 30)
    wait.until(lambda driver: browser.execute_script("return jQuery.active == 0"))


def get_action_message(browser, xpath):
    """
        wait for action to complete and return message
    """
    wait_for_ajax_to_complete(browser)
    return get_text_by_xpath(browser, xpath)


def check_radio_button(browser, xpath):
    """
        check radio button
    """
    is_checked = None
    try:
        is_checked = find_element_by_xpath(browser, xpath).get_attribute("checked")
    except:
        pass

    if not is_checked:

        ActionChains(browser).move_to_element(find_element_by_xpath(browser, xpath)).click().perform()


def scroll_page(browser, position):
    """
        Scroll page on the y-axis at given position
    """
    browser.execute_script("scroll(0, {position})".format(position=position))


def check_box(browser, xpath, check):
    is_checked = None
    try:
        is_checked = find_element_by_xpath(browser, xpath).get_attribute("checked")
    except:
        pass

    if not is_checked and check:
        ActionChains(browser).move_to_element(find_element_by_xpath(browser, xpath)).click().perform()

    if is_checked and not check:
        ActionChains(browser).move_to_element(find_element_by_xpath(browser, xpath)).click().perform()




