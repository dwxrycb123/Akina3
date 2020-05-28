from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *
from wrappers import *

@on_command('announce', aliases=('公告', ), only_to_me=False)
@normal_command('weather', only_in_group=False)
async def annouce(session: CommandSession, user: User, group: Group):
    content = session.get('content')
    msg = "[秋菜酱的公告]\n{}".format(content)
    for g_id in GROUP_INFORMED:
        await nonebot._bot.send_group_msg(group_id=g_id, message=msg)
    
    return 

    # 

@annouce.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    session.state["content"] = stripped_arg
    return 


