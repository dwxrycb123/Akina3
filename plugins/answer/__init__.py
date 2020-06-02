from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *

import aiocqhttp
from aiocqhttp import CQHttp
import random
import numpy as np


@nonebot._bot.on_message
async def answer(event: aiocqhttp.Event):
    # keywords like '抽！' also has to be considered, maybe we can write a commandController to register these things automatically
    if str(event['message']) == '单次抽卡':
        return 
    if event.detail_type != 'group':
        print("not a group message, no need to answer")
        return 

    # print(event)
    msg = str(event['message'])
    group_id = event['group_id']
    user_id = event['user_id']

    if not record_and_check_operation(user_id, "answer", msg):
        return 
    
    print(event)
    print("group_id={}".format(group_id))
    print("msg={}".format(msg))    
    # if group_id == 680249834:
    #     await nonebot._bot.send_group_msg(group_id=group_id, message='小木曾雪菜天下第一！')
    group = await Group().getGroup(group_id)
    user = await User().getUser(user_id)
    if group.auth < ANSWER_AUTH:
        return 
    

    Qs = await table_question_info.select_record({
        'question': msg,
        'env': group_id
    })
    Qs += await table_question_info.select_record({
        'question': msg,
        'env': 'global' 
    })

    print(Qs)
    if not len(Qs):
        return 
    Q_prob = np.array([float(q['prob']) for q in Qs])
    Q_prob /= Q_prob.sum()
    Qs = np.random.choice(Qs, p=Q_prob)
    if random.uniform(0, 1) >= float(Qs['prob']):
        return 
    _env = Qs['env']
    
    As = await table_teach.select_record({
        'question': msg,
        'env': _env
    })
    print(As)

    if not len(As):
        await table_question_info.delete_record({
            'question': msg,
            'env': _env
        })
        print('the question has no answer, thus has been deleted.')
        return 

    p = np.array([float(x['prob']) for x in As])
    p /= p.sum()
    
    c = np.random.choice(As, p=p)
    print(c)


    name = user.nickname if user.nickname != NO_NICKNAME else event['sender']['nickname']
    text = c['answer'].replace('$s', name).replace('\s', ' ')
    
    # await nonebot._bot.send_group_msg(group_id=group_id, message=text)
    await send_group_msg_with_delay(group_id, text)
    
    return 



