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

pattern_lookup = ArgPattern('lookup', '<item_name:str>')
patterns = [pattern_lookup]

@on_command('lookup', aliases=('查看',), only_to_me=False)
@normal_command('lookup', only_in_group=False)
async def lookup(session: CommandSession, user: User, group: Group):
    result = session.state.get("result")
    if result["name"] == "lookup":
        pass
    user_id = user.user_id
    user_info = await get_info(user_id)
    items = await get_items_info()

    for _ in items:
        if _["name"] == result["item_name"]:
            if str(_["id"]) not in user_info["items"]:
                msg = "还没有抽到过这个奖品呢."
            else:
                msg = "{}({}): 当前拥有{}件\n{}".format(_["name"], _["rarity"], user_info["items"][str(_["id"])], _["description"])
            await session.send(msg)
            return 
    await session.send("未找到该物品.")

@lookup.args_parser
@args_pattern_parser(patterns)
async def _(session: CommandSession):
    pass