from modules.automation.autobot.config import payloads as pl
from modules.automation.autobot.config import constants as const
from modules.automation.autobot.lib import restAPIs as rapi

api = rapi.project_create()
url = util.create_running_url(const.lp_addr, api)
header = const.header
payload = pl.project(const.project_name, const.project_desc)

print(url)
print(header)
print(payload)



