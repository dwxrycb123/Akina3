import os
import json
import aiofiles

from config import * 
from database.jsonio import *
async def get_items_info():
    return await get_json(ITEM_DATAPATH)
