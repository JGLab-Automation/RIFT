from autobot.lib import framework as fw
from autobot.lib import utility as util
from autobot.lib import restAPIs as rapi
from autobot.config import constants as const
from autobot.config import payloads as pl




api = rapi.project_create()
url = util.create_running_url(const.lp_addr, api)
header = const.header
payload = pl.project(const.project_name, const.project_desc)

print(url)
print(header)
print(payload)



