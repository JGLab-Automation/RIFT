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


def get_config(url, header, payload=""):
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        log_info("Fetching configuration.")
        response = requests.request("GET", url=url, headers=header, data=payload, verify=False)
        if response.status_code == 200:         # Code for successful response.
            data = response.json()
            log_info(f"Data received: {data}.")
            return data
        elif response.status_code == 204:       # Code for response with 'No Content'.
            data = response.json()
            log_info(f"Data received: {data}.")
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
        log_info("Adding configuration")
        response = requests.request("POST", url=url, headers=header, data=payload, verify=False)
        if response.status_code == 201:
            data = response.json()
            log_info(f"Data received: {data}.")
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
        log_info("Editing configuration.")
        response = requests.request("PUT", url=url, headers=header, data=payload, verify=False)
        if response.status_code == 201:
            data = response.json()
            log_info(f"Data received: {data}")
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
        log_info("Deleting configuration.")
        response = requests.request("DELETE", url=url, headers=header, data=payload, verify=False)
        if response.status_code == 201:
            data = response.json()
            log_info(f"Data received: {data}")
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










def create_html_mail(html, Subject, fromEmail, toEmail, cc=None, attachment=None):
    """Create a mime-message that will render HTML in popular
    MUAs, text in better ones"""
    #copy_email_tos = ''
    #cc1 = ''
    msg = MIMEMultipart('alternative')
    msg['From'] = fromEmail
    msg['To'] = toEmail
    msg['Subject'] = Subject
    msg.attach(MIMEText(html))
    if cc:
        msg['Cc'] = cc.strip(',')
    if attachment:
        ctype, encoding = mimetypes.guess_type(attachment)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            fp = open(attachment)
            # Note: we should handle calculating the charset
            att = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
            att.add_header('Content-Disposition', 'attachment; filename=' + attachment.split('/')[-1])
            msg.attach(att)
        elif maintype == 'image':
            fp = open(attachment, 'rb')
            att = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
            att.add_header('Content-Disposition', 'attachment; filename=' + attachment.split('/')[-1])
            msg.attach(att)
        elif maintype == 'audio':
            fp = open(attachment, 'rb')
            att = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
            att.add_header('Content-Disposition', 'attachment; filename=' + attachment.split('/')[-1])
            msg.attach(att)
        elif maintype == 'application':
            fp = open(attachment, 'rb')
            att = MIMEApplication(fp.read(), _subtype=subtype)
            fp.close()
            att.add_header('Content-Disposition', 'attachment; filename=' + attachment.split('/')[-1])
            msg.attach(att)
        else:
            fp = open(attachment, 'rb')
            att = MIMEBase(maintype, subtype)
            att.set_payload(fp.read())
            # Encode the payload using Base64
            encoders.encode_base64(att)
            att.add_header('Content-Disposition', 'attachment; filename=' + attachment.split('/')[-1])
            msg.attach(att)
            fp.close()
        # Set the filename parameter

    html_part = MIMEText(html, 'html')
    msg.attach(html_part)
    log(msg)
    return msg


def send_email(message, send_from, send_tos, subject='', cc=None, attachment=None, smtp_server='mail.office.com'):

     # RECIPIENTS = send_tos
    log_info('Sending email to ' + send_tos)
    recipients = send_tos.split(',')
    sender = send_from
    msg = create_html_mail(message, subject, send_from, send_tos, cc, attachment)

    auth_required = 0  # if you need to use SMTP AUTH set to 1
    smtp_user = ''  # for SMTP AUTH, set SMTP username here
    smtp_pass = ''  # for SMTP AUTH, set SMTP password here
    session = smtplib.SMTP(smtp_server)
    if auth_required:
        session.login(smtp_user, smtp_pass)
    smtp_result = session.sendmail(sender, recipients, msg.as_string())
    session.quit()

    if smtp_result:
        return 0
    else:
        return 1

