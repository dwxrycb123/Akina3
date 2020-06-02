from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *

import datetime

async def search_by_QA(question, answer, env=None):
    print("search env={}".format(env))
    if env is None:
        result = await table_teach.select_record({
            'question': question,
            'answer': answer
        })
        return result
    result = await table_teach.select_record({
        'question': question,
        'answer': answer,
        'env': env
    })
    if env != 'global':
        result += await table_teach.select_record({
            'question': question,
            'answer': answer,
            'env': 'global'
        })
    return result

async def search_by_Q_or_A(string, env=None):
    print("search env={}".format(env))
    result_q = await table_teach.select_record({
        'question' : string,
        'env': env
    })
    result_a = await table_teach.select_record({
        'answer': string,
        'env': env
    })
    '''
    if env != 'global':
        result_q += await table_teach.select_record({
            'question': string,
            'env': 'global'
        })
        result_a += await table_teach.select_record({
            'answer': string
        })
    '''
    return result_q, result_a

