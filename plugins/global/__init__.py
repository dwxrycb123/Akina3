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
from wrappers import *

@nonebot._bot.on_message
async def global_alias(event: aiocqhttp.Event):
    await lottery(event)


@global_command("lottery", aliases=["单次抽卡", "单抽", "抽卡", "抽！"], only_in_group=True)
async def lottery(event: aiocqhttp.Event, user: User, group: Group):
    c, is_first = await give_item(user.user_id)
    _msg = msg_of_lottery(user.nickname, c, is_first)
    await usr_group_send_msg_with_delay(user, group, _msg + '\n' + format(c['description']))