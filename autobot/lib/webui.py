__author__ = "JG"

from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.config import xpaths as xp


def login(browser, lp_addr, uname, passwd):
    try:
        util.log_info(f"Login to- {lp_addr}.")
        fw.go_to_url(browser, lp_addr)
        util.log_info(f"Login with username- {uname}.")
        fw.input_by_xpath(browser, xp.login_uname, uname)
        fw.input_by_xpath(browser, xp.login_passwd, passwd)
        fw.click_button(browser, xp.login_button)
        fw.wait_for_ajax_to_complete(browser)
    except BaseException as e:
        util.log_info(e)
        raise


#def add_cloud_account(browser)