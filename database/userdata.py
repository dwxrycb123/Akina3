import os
import json
import aiofiles
from database.jsonio import *
# items
# user's owned items:
# kokemans
# user's owned kokemans

# property (余额)
# items （物品）
# kokemans（kokeman）
# 好感度（不急）
# 成就系统（不急）
from config import * 

async def get_info(user_id):
    filename = str(user_id) + '.json'
    filepath = os.path.join(USER_DATAPATH, filename)
    if not os.path.exists(filepath):
        # write default info
        j = dict()
        j['items'] = {}
        j['property'] = 10
        j['kokemans'] = []
        j['achievements'] = []
        await save_info(user_id, j)
        return j
    
    return await get_json(filepath)

async def save_info(user_id, data):
    filename = str(user_id) + '.json'
    filepath = os.path.join(USER_DATAPATH, filename)
    await save_json(filepath, data)