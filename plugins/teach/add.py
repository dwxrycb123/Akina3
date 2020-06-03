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

async def add_QA(result, session):
        if not result['answer_probability']:
            result['answer_probability'] = 1.0
        if not result['question_probability']:
            result['question_probability'] = 1.0

        env = session.event.group_id if not result['global'] else 'global'
        search_result = await search_by_QA(result['question'], result['answer'], env)
        if len(search_result):
            await session.send(TEACH_ALREADY_EXISTS_MSG)
            return 
        
        await table_teach.add_record({
            'question': result['question'],
            'answer': result['answer'],
            'prob': result['answer_probability'],
            'env': env,
            'create_date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'author_id': session.event.user_id if not result['anonymous'] else 0
        })

        await question_info_safe_update(result['question'], env, result['question_probability'] or 1.0)

        new_id = await search_by_QA(result['question'], result['answer'], env)
        new_id = new_id[0]['id']
        await session.send('问答已添加，编号为{}.'.format(new_id))
        return 