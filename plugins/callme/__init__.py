from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *
from wrappers import * 


@on_command('callme', aliases=('叫我', '我叫'), only_to_me=False)
@normal_command('callme', only_in_group=False)
async def callme(session: CommandSession, user: User, group: Group):
    # user = await User().getUser(session.event.user_id)
    nickname = session.get('nickname', prompt="秋菜酱应该叫你什么呢x")

    await user.set('nickname', nickname)

    await session.send('好的，{}，请多指教！'.format(nickname))

@callme.args_parser
@args_pattern_parser(patterns)
async def _(session: CommandSession):
    pass
    



