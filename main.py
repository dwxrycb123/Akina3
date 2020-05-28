import nonebot 
from nonebot import on_command, scheduler, CommandSession, message, on_startup
import config 
import os

import asyncio

from models.model import * 
from database.mysql import *
from database.tables import *


    
if __name__ == '__main__':
    nonebot.init(config)

    nonebot.load_builtin_plugins()

    nonebot.load_plugins(os.path.join('.', 'plugins'), 'plugins')
    nonebot.run(host='0.0.0.0', port=8000)    