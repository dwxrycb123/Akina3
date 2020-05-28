from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *
from wrappers import *

import os, sys
sys.path.append(os.path.dirname(__file__))
from get_weather import get_weather_msg

weather_pattern = ArgPattern('weather', '<city:str> [-t|--tomorrow]')
patterns = [weather_pattern]

@on_command('weather', aliases=('天气', '查天气'), only_to_me=False)
@normal_command('weather', only_in_group=False)
async def weather(session: CommandSession, user: User, group: Group=None):
    result = session.get('result')
    city = result['city']
    tomorrow = result['tomorrow']

    msg = await get_weather_msg(city, tomorrow)
    await session.send(msg)

@weather.args_parser
@args_pattern_parser(patterns)
async def _(session: CommandSession):
    pass