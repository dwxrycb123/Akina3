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


@on_command('system', aliases=(), only_to_me=False)
@normal_command('system', only_in_group=False)
async def system(session: CommandSession, user: User, group: Group):
    await session.send(str(BLOCK_OFF))