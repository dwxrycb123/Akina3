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

async def query(result, session):
    if result['keyword']:
        return 
    result_q, result_a = await search_by_Q_or_A(result['question_or_answer'], session.event['group_id'])
    result_q_g, result_a_g = await search_by_Q_or_A(result['question_or_answer'], 'global')

    if len(result_q)+len(result_q_g):
        msg = '以{}为问题的回答有：\n'.format(result['question_or_answer'])
        for r in result_q:
            msg += str(r['id']) + '. ' + r['answer'] + '\n'
        for r in result_q_g:
            msg += str(r['id']) + '. ' + r['answer'] + ' [global]\n'
    else:
        msg = '未找到以{}为问题的回答.\n'.format(result['question_or_answer'])
    if len(result_a)+len(result_a_g):
        msg += '以{}为回答的问题有：\n'.format(result['question_or_answer'])
        for r in result_a:
            msg += str(r['id']) + '. ' + r['question'] + '\n'
        for r in result_a_g:
            msg += str(r['id']) + '. ' + r['question'] + ' [global]\n'
    else:
        msg += '未找到以{}为回答的问题.'.format(result['question_or_answer'])
    
    if msg[-1] == '\n':
        msg = msg[:-1]
    await session.send(msg)
    return 