from database.mysql import *
from database.tables import *
from models.model import *

import nonebot 
from nonebot import on_command, scheduler, CommandSession, message, on_startup

@on_startup
async def start_up():

    # database
    loop = asyncio.get_event_loop()
    testdb.set_loop(None)
    await testdb.create_pool()
    User.set_config(testdb, table_user_info, table_user_command_times)
    Group.set_config(testdb, table_group_info)
    # pass