from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *
from database.itemdata import *
from database.userdata import *

import os, sys
from config import *
import numpy as np

async def choose_item():
    rarity = ['N', 'R', 'SR', 'SSR']
    choose_rarity = np.random.choice(rarity, p=[LOTTERY_N_PROB, LOTTERY_R_PROB, LOTTERY_SR_PROB, LOTTERY_SSR_PROB])
    items = await get_items_info()
    _items = []
    for _ in items:
        if _['rarity'] == choose_rarity:
            _items.append(_)
    
    return np.random.choice(_items)


async def give_item(user_id):
    c = await choose_item()
    user_info = await get_info(user_id)
    if str(c["id"]) in user_info['items']:
        user_info['items'][str(c['id'])] += 1
        is_first = False
    else:
        user_info['items'][str(c['id'])] = 1
        is_first = True
    await save_info(user_id, user_info)
    return c, is_first

def msg_of_lottery(nickname, item, is_first):
    raw_msg = "恭喜 {} 获得 {}({}) ！"
    if is_first:
        raw_msg = "恭喜 {} 获得了新物品 {}({})！"
    msg = raw_msg.format(nickname, item['name'], item['rarity'])
    return msg