from nonebot import on_command, CommandSession, argparse
import aiocqhttp

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *
from util import *
from typing import List, Callable

from functools import wraps

def normal_command(command_name: str, only_in_group: bool=False) -> callable:
    """
    command_name: str, the name of the command, used to get information like CD time or the calling times limit \
    only_in_group: bool=False, whether the command is only activated in group environment 
    """

    def deco(func: callable):
        @wraps(func)
        async def wrapped_func(session: CommandSession):
            # print("raw msg: {}".format(session.event.raw_message))
            group = None

            if only_in_group and session.event.detail_type != 'group':
                print("command {}: not a group message, ignore (since only_group=True)")
                return 
            if session.event.detail_type == 'group':
                group = await Group().getGroup(session.event.group_id)
            
            auth, user = await get_auth_and_user(session)
            command_auth = CMD_AUTH[command_name]

            if not await check_cmd_times(user, command_name):
                session.send(TIMES_UP_MSG)
                return False
            
            if not check_CD(user, command_name):
                await session.send(IN_CD_MSG.format(CMD_CD[command_name]))
                return 
            
            if not record_and_check_operation(user.user_id, command_name, str(session.event.raw_message)):
                print("block mechanism has been activated")
                return 
            
            if auth < command_auth:
                await session.send(LOW_AUTH_MSG)
                return 
            
            await func(session, user, group)

        return wrapped_func
    
    return deco 

def args_pattern_parser(patterns: List[ArgPattern]):
    """
    patterns: all the patterns of the commands, a list of ArgPattern instances
    """
    def deco(func: callable):
        @wraps(func)
        async def wrapped_func(session: CommandSession):
            stripped_arg = session.current_arg_text.strip()
            print('stripped_arg={}'.format(stripped_arg))

            for p in patterns:
                result = p.parse(stripped_arg)
                if result is not None:
                    session.state["result"] = result
                    
                    await func(session)
                    return 
            
            session.finish(ARGUMENT_ERROR_MSG)
        
        return wrapped_func
    
    return deco

def global_command(command_name: str, aliases: List[str], only_in_group: bool=False) -> callable:
    """
    command_name: str, the name of the command, used to get information like CD time or the calling times limit \
    only_in_group: bool=False, whether the command is only activated in group environment 
    """

    def deco(func: callable):
        @wraps(func)
        async def wrapped_func(event: aiocqhttp.Event):
            group = None 
            user = await User().getUser(event['user_id'])

            if only_in_group and event.detail_type != 'group':
                print("command {}: not a group message, ignore (since only_group=True)")
                return 
            if event.detail_type == 'group':
                group = await Group().getGroup(event.group_id)
            
            is_called = False
            msg = str(event['message'])
            for s in aliases + [head + command_name for head in COMMAND_START]:
                if msg[:len(s)] == s:
                    is_called = True
                    msg = msg[len(s):]
                    break 
            
            if not is_called:
                return 

            if msg.strip() != "":
                return 
            
            cd_check = await check_cd_times(user, group, command_name)
            if not cd_check:
                return 
            auth_check = await check_auth(user, group, CMD_AUTH[command_name])
            if not auth_check:
                await usr_group_send_msg_with_delay(user, group, LOW_AUTH_MSG)
                return 
            
            await func(event, user, group)
        
        return wrapped_func
    
    return deco