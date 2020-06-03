from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *

import datetime

import os, sys


async def question_info_safe_update(question, env, prob):
    question = str(question)
    env = str(env)
    prob = str(prob)
    
    ret = await table_question_info.select_record({
        'question': question,
        'env': env,
    })
    if not len(ret):
        ret = await table_question_info.add_record({
            'question': question,
            'env': env,
            'prob': prob
        })
    else:
        if len(ret)>1:
            # delete
            await table_question_info.delete_record({
                'question': question,
                'env': env,
            })
            ret = await table_question_info.add_record({
                'question': question,
                'env': env,
                'prob': prob
            })
        else:
            ret = await table_question_info.update_record({
                'prob' : prob
            },
            {
                'question': question,
                'env': env,
            })