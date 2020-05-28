from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *
from wrappers import *


import os, sys
sys.path.append(os.path.dirname(__file__))
from choose import *


@on_command('times', aliases=('调用次数', '查询调用次数'), only_to_me=False)
@normal_command('times', only_in_group=False)
async def times(session: CommandSession, user: User, group: Group=None):
    msg = "{}, 你的剩余调用次数为：\n".format(user.nickname)
    for cmd in CMD_TIMES:
        msg += "{}: {}\n".format(cmd, getattr(user, cmd))
    if msg[-1] == '\n':
        msg = msg[:-1]
    await session.send(msg)
