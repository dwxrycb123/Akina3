from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *

import datetime

import os, sys
sys.path.append(os.path.dirname(__file__))
from search import *

async def delete(result, session):
    await table_teach.delete_record({
        'id': result['index']
    })
    await session.send("编号为{}的问答已删除.".format(result['index']))
