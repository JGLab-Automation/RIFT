__author__ = 'JG'

import logging
import urllib3
import requests
from requests.auth import HTTPBasicAuth
import json
import smtplib
import inspect
import time
import sys
import os
import re


logger = logging.getLogger(__name__)


def log(text, level='debug'):
    if level.lower() == 'debug':
        logger.debug(text)
        return
    elif level.lower() == 'info':
        logger.info(text)
    elif level.lower() == 'critical':
        logger.critical(text)
    elif level.lower() == 'error':
        logger.error(text)
    elif level.lower == 'warning':
        logger.warning(text)
    print (text)


def log_info(text):
    log(text, 'info')


def log_debug(text):
    log(text, 'debug')


def log_error(text):
    log(text, 'error')


def create_operational_url(lp_addr, api):
    try:
        url = f'https://{lp_addr}:8008/api/operational/{api}'
        return str(url).strip()
    except BaseException as e:
        log_info(e)
        raise


def create_operations_url(lp_addr, api):
    try:
        url = f'https://{lp_addr}:8008/api/operations/{api}'
        return str(url).strip()
    except BaseException as e:
        log_info(e)


def create_running_url(lp_addr, api):
    try:
        url = f'https://{lp_addr}:8008/api/running/{api}'
        return str(url).strip()
    except BaseException as e:
        log_info(e)


def create_http_basic_auth(uname, passwd):
    try:
        auth = HTTPBasicAuth(uname, passwd)
        return (auth)
    except BaseException as e:
        log_info(e)
        raise


def get_config(url, header, payload=""):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.request("GET", url=url, headers=header, verify=False)
        if response.status_code != 200:
            assert response.status_code == 200, f'Response is: {response.status_code}.'
        else:
            data = response.json()
            return (data)
    except BaseException as e:
        log_info(e)
        raise


def create_config(url, header, payload):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.request("POST", url=url, headers=header, data=payload, verify=False)
        if response.status_code != 201:
            assert response.status_code == 201, f'Response is: {response.status_code}.'
        else:
            data = response.json()
            return (data)
    except BaseException as e:
        log_info(e)
        raise


def edit_config(url, header, payload):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.request("PUT", url=url, headers=header, data=payload, verify=False)
        if response.status_code != 201:
            assert response.status_code == 201, f'Response is: {response.status_code}.'
        else:
            data = response.json()
            return (data)
    except BaseException as e:
        log_info(e)
        raise


def delete_config(url, header, payload=""):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        response = requests.request("DELETE", url=url, headers=header, data=payload, verify=False)
        if response.status_code != 201:
            assert response.status_code == 201, f'Response is: {response.status_code}.'
        else:
            data = response.json()
            return (data)
    except BaseException as e:
        log_info(e)
        raise






















def read_json(file_name, node):
    json_data = open(file_name)
    data = json.load(json_data)
    json_data.close()
    return data[node]


# def is_valid_xml(xml_file):
#     try:
#         et.parse(xml_file)
#         return True
#     except Exception as e:
#         return False

def parse_xml(xml_file, *attributes):
    if not os.path.exists(xml_file):
        log("XML does not exist")
        return []
    tree = et.parse(xml_file)
    root = tree.getroot()
    values = []
    for child in root:
        attr_list = child.attrib
        row = ''
        if not len(attributes):
            for key in attr_list:
                try:
                    row += attr_list[key] + ', '
                except StandardError:
                    row += ', '
        else:
            for attribute in attributes:
                try:
                    row += attr_list[attribute] + ', '
                except StandardError:
                    row += ', '
        if not row == '':
            values.append(row+'\n')
    return values