from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *
from wrappers import *

import datetime

import os, sys
sys.path.append(os.path.dirname(__file__))
from search import *
from query import *
from add import *
from delete import *
from edit import *
# '<question:str> <answer:str> [-p|--answer_prob:float] [-P|--question_prob:float] [-a|--anonymous]'
pattern_QA = ArgPattern('QA', '<question:str> <answer:str> [-g|--global] [-p|--answer_probability:float] [-P|--question_probability:float] [-a|--anonymous]')
pattern_edit = ArgPattern('Edit', '(-e|--edit) <index:int> [-g|--global] [-A|--answer:str] [-Q|--question:str]  [-p|--answer_probability:float] [-P|--question_probability:float]')
pattern_query_QA = ArgPattern('Query_QA', '(-q|--query) <question_or_answer:str> [-k|--keyword]')
pattern_delete_id = ArgPattern('Delete_id', '(-d|--delete) <index:int>')

patterns = [pattern_QA, pattern_edit, pattern_query_QA, pattern_delete_id]

@on_command('teach', aliases=('教学'), only_to_me=False)
@normal_command('teach', only_in_group=True)
async def teach(session: CommandSession, user: User, group: Group):

    # user = await User().getUser(session.event.user_id)
    result = session.get('result')
    print("result:"+str(result))
    # await session.send(str(result))
    if result['name'] == 'QA':
        await add_QA(result, session)
        return 
    if result['name'] == 'Edit':
        await edit(result, session)
        return 
    if result['name'] == 'Query_QA':
        await query(result, session)
        return 
    if result['name'] == 'Delete_id':
        await delete(result, session)
        return 
    
    raise AssertionError('Unknown pattern name founded')
    return 

@teach.args_parser
@args_pattern_parser(patterns)
async def _(session: CommandSession):
    pass