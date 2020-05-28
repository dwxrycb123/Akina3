import nonebot

from database.mysql import *
from database.tables import * 
from models.model import *

from config import *

@nonebot.scheduler.scheduled_job('cron', day='*')
async def clear_command_times():
    record = await table_user_command_times.select_record('TRUE')
    for item in record:
        await table_user_command_times.update_record(CMD_TIMES, item)
    print('command times cleared!')
