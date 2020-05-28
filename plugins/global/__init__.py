from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *
import aiocqhttp
from aiocqhttp import CQHttp
import random
import numpy as np

import os, sys
sys.path.append(os.path.dirname(__file__))
from choose import *

@nonebot._bot.on_message
async def global_alias(event: aiocqhttp.Event):

    if event.detail_type != 'group':
        print("not a group message, no need to answer")
        return 
    
    user_id = event['user_id']
    group_id = event['group_id']    
    if str(event['message']) == '单次抽卡' or str(event['message']) == '#!lottery':
        user = await check_auth_cd_times(user_id, group_id, auth_needed=LOTTERY_AUTH, cmd_name="lottery")
        if not user:
            return 

        auth_check = await check_auth(user_id, group_id, LOTTERY_AUTH)
        if not auth_check:
            return False

        c = await give_item(user_id)
        _msg = msg_of_lottery(user.nickname, c)
        await send_group_msg_with_delay(group_id=group_id, msg=_msg + '\n' + format(c['description']))


