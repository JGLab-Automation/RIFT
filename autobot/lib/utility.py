__author__ = 'JG'

import logging
import urllib3
import urllib.parse
import urllib.request
import requests
from requests.auth import HTTPBasicAuth
import json
import smtplib
import inspect
import time
import sys
import os
import re
import mimetypes
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


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


def api_url(lp_addr, api):
    try:
        url = f'https://{lp_addr}:8008/{api}'
        return str(url).strip()
    except BaseException as e:
        log_info(e)


def generate_log(url, header, payload=""):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.request("GET", url=url, headers=header, data=payload, verify=False)
        if response.status_code == 200:         # Code for successful response.
            data = response.text
            return data
        else:
            data = response.text
            assert response.status_code == 200, f"Response: {response.status_code} | Data received: {data}."
    except BaseException as e:
        log_info(e)
        raise


def download_file(url, filename="autobot/artifacts/traces/rift.log"):
    try:
        #filename = "autobot/artifacts/traces/rift.log"
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        x = urllib.request.urlretrieve(url, filename)
        print(x)
    except BaseException as e:
        log_info(e)
        raise


def create_url_running(lp_addr, api):
    try:
        url = f'https://{lp_addr}:8008/api/running/{api}'
        return str(url).strip()
    except BaseException as e:
        log_info(e)


def create_url_operations(lp_addr, api):
    try:
        url = f'https://{lp_addr}:8008/api/operations/{api}'
        return str(url).strip()
    except BaseException as e:
        log_info(e)


def create_url_operational(lp_addr, api):
    try:
        url = f'https://{lp_addr}:8008/api/operational/{api}'
        return str(url).strip()
    except BaseException as e:
        log_info(e)
        raise


def create_http_basic_auth(uname, passwd):
    try:
        auth = HTTPBasicAuth(uname, passwd)
        return auth
    except BaseException as e:
        log_info(e)
        raise


def get_encoded_url(value):
    try:
        query = urllib.parse.quote(value, safe='')
        return query
    except BaseException as e:
        log_info(e)
        raise


def get_config(url, header, payload=""):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.request("GET", url=url, headers=header, data=payload, verify=False)
        if response.status_code == 200:         # Code for successful response.
            data = response.json()
            # log_info(f"Data received: {data}.")
            return data
        elif response.status_code == 204:       # Code for response with 'No Content'.
            # data = response.json()
            # log_info(f"Data received: {data}.")
            return None
        else:
            data = response.json()
            assert response.status_code == 200, f"Response: {response.status_code} | Data received: {data}."
    except BaseException as e:
        log_info(e)
        raise


def add_config(url, header, payload):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.request("POST", url=url, headers=header, data=payload, verify=False)
        if response.status_code == 201:
            data = response.json()
            return data
        else:
            data = response.json()
            assert response.status_code == 201, f"Response: {response.status_code} | Data received: {data}."
    except BaseException as e:
        log_info(e)
        raise


def edit_config(url, header, payload):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.request("PUT", url=url, headers=header, data=payload, verify=False)
        if response.status_code == 201:
            data = response.json()
            return data
        else:
            data = response.json()
            assert response.status_code == 201, f"Response: {response.status_code} | Data received: {data}."
    except BaseException as e:
        log_info(e)
        raise


def delete_config(url, header, payload=""):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.request("DELETE", url=url, headers=header, data=payload, verify=False)
        if response.status_code == 201:
            data = response.json()
            return data
        else:
            data = response.json()
            assert response.status_code == 201, f"Response: {response.status_code} | Data received: {data}."
            log_info(f"Response received: {response.text}.")

    except BaseException as e:
        log_info(e)
        raise


def get_rpc_state(status):
    key1 = list(status.keys())
    key2 = list(status[key1[0]].keys())
    state = key2[0]
    return state


def get_rpc_error_state(status):
    val1 = list(status.values())
    val2 = list(val1[0].values())
    val3 = list(val2[0].values())
    state = val3[1]
    return state


def get_transac_id(status):
    val1 = list(status.values())
    val2 = list(val1[0].values())
    id = val2[0]
    return id


def get_nsr_id(status):
    val1 = list(status.values())
    val2 = list(val1[0].values())
    id = val2[0]
    return id


def get_ns_transac_status(status):
    val1 = list(status.values())
    val2 = list(val1[1].values())
    state = val2[0]
    return state









def create_html_mail(html, subject, fromEmail, toEmail, cc=None, attachment=None):
    """Create a mime-message that will render HTML in popular
    MUAs, text in better ones"""
    #copy_email_tos = ''
    #cc1 = ''
    msg = MIMEMultipart('alternative')
    msg['From'] = fromEmail
    msg['To'] = toEmail
    msg['Subject'] = subject
    if cc:
        msg['Cc'] = cc.strip(',')
    if attachment:
        fp = open(attachment, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
    html_part = MIMEText(html, 'html')
    msg.attach(html_part)
    log(msg)
    return msg


def send_email(message, send_from, send_tos, subject='', cc=None, attachment=None, smtp_server='smtp.office365.com'):

     # RECIPIENTS = send_tos
    log_info('Sending email to ' + send_tos)
    recipients = send_tos.split(',')
    sender = send_from
    msg = create_html_mail(message, subject, send_from, send_tos, cc, attachment)

    auth_required = 0  # if you need to use SMTP AUTH set to 1
    smtp_user = ''  # for SMTP AUTH, set SMTP username here
    smtp_pass = ''  # for SMTP AUTH, set SMTP password here
    session = smtplib.SMTP(smtp_server)
    #session = smtplib.SMTP_SSL("smtp.office365.com", 587)
    if auth_required:
        session.login(smtp_user, smtp_pass)
    smtp_result = session.sendmail(sender, recipients, msg.as_string())
    session.quit()

    if smtp_result:
        return 0
    else:
        return 1

