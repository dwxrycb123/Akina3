from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *
from wrappers import *

from database.userdata import *
from database.itemdata import *

import os, sys
sys.path.append(os.path.dirname(__file__))
from choose import *


@on_command('asset', aliases=('我的仓库', '我的物品'), only_to_me=False)
@normal_command('asset', only_in_group=False)
async def asset(session: CommandSession, user: User, group: Group):
    user_id = user.user_id
    user_info = await get_info(user_id)
    assets = user_info['items']
    items = await get_items_info()
    msg = "{}，你拥有{}件物品中的{}件。\n".format(user.nickname, len(items), len(assets))
    for rarity in ['N', 'R', 'SR', 'SSR']:
        msg+='{}: '.format(rarity)
        for index in assets:
            _ = items[int(index)]
            if _['rarity'] == rarity:
                msg += "{}×{}; ".format(_['name'], assets[index])
        msg += '\n'
    if msg[-1] == '\n':
        msg = msg[:-1]
    await session.send(msg)
