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
from question_info import *

# -o --only_answer ; do not update question_info when receive this flag
async def edit(result, session):
    teach_info_ = dict()
    question_info_ = dict()

    
    original_qa = await table_teach.select_record({
        'id': result['index']
    })
    original_qa = original_qa[0]

    original_q = await table_teach.select_record({
        'question': original_qa['question'],
        'env': original_qa['env']
    })
    original_q = original_q[0]
    
    question_info_['env'] = original_q['env']
    question_info_['question'] = original_q['question']
    question_info_['prob'] = original_q['prob']

    if result['question_probability']:
        question_info_['prob'] = result['question_probability']
    if result['question']:
        teach_info_['question'] = result['question'] 
        question_info_['question'] = result['question']
    if result['answer']:
        teach_info_['answer'] = result['answer']
    if result['answer_probability']:
        teach_info_['prob'] = result['answer_probability']
    if result['global']:
        teach_info_['env'] = 'global'
        question_info_['env'] = 'global'

    try:
        await table_teach.update_record(teach_info_,
        {
            'id': result['index']
        })
    except Exception as e:
        print(e)
        print("no need to update table_teach")

    try:
        await question_info_safe_update(question_info_['question'], question_info['env'], question_info['prob'])
        # await table_question_info.add_record(question_info_)
    except Exception as e:
        print(e)
    
    await session.send('编号为{}的问答已修改.'.format(result['index']))
    return 
    