from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *

from util import *
from wrappers import *


@on_command('greet', aliases=(), only_to_me=False)
@normal_command('greet', only_in_group=False)
async def greet(session: CommandSession, user: User, group: Group):
    if user.nickname == NO_NICKNAME:
        await session.send('唔姆，秋菜酱还不知道你叫什么呢')
    else:
        await session.send('你好呀，{}!'.format(user.nickname))