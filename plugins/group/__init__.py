from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *
from wrappers import * 


pattern_set_authority = ArgPattern('set_authority', '(-a|--authority) <index:int>')
patterns = [pattern_set_authority]

@on_command('group', aliases=('群权限',), only_to_me=False)
@normal_command('weather', only_in_group=True)
async def group(session: CommandSession, user: User, group: Group):
    result = session.get('result')
    if result['name'] == 'set_authority':
        _group = await Group().getGroup(session.event.group_id)
        await _group.set('auth', result['index'])
        await session.send("群权限已调整为{}".format(result["index"]))


@group.args_parser
@args_pattern_parser(patterns)
async def _(session: CommandSession):
    pass

