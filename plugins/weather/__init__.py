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

@on_command('weather', aliases=('天气', '查天气'), only_to_me=False)
@normal_command('weather', only_in_group=False)
async def weather(session: CommandSession, user: User, group: Group=None):
    city = session.get('city')
    tomorrow = session.get('tomorrow')

    msg = await get_weather_msg(city, tomorrow)
    await session.send(msg)

@weather.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    print('stripped_arg={}'.format(stripped_arg))
    result = weather_pattern.parse(stripped_arg)
    print("result={}".format(result))
    if result is None:
        session.finish(ARGUMENT_ERROR_MSG)

    session.state["city"] = result["city"]
    session.state["tomorrow"] = result["tomorrow"]