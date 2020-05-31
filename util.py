import nonebot
from nonebot import on_command, CommandSession, argparse

from database.mysql import * 
from database.tables import *
from models.model import *
from config import *

import asyncio
import re
import copy
import time

async def get_auth_and_user(session: CommandSession):
    user_id = session.event.user_id
    group_id = session.event.group_id
    auth = 0

    user =  await User().getUser(user_id)
    if group_id:
        group = await Group().getGroup(group_id)
        auth = max(auth, group.auth)

    auth = max(auth, user.auth)

    if user_id in SUPERUSERS:
        auth = 6

    return auth, user

async def check_cmd_times(user: User, command_name: str):
    if command_name not in CMD_TIMES:
        return True
    current_times = getattr(user, command_name) 
    if current_times >= 1:
        await user.set(command_name, current_times - 1)
        return True
    else:
        return False

def parse_value(string, value_type='str'):
    '''
    parse a value string with the given value type.
    if value_type has some value other than 'string' or 'int', None will be returned.
    '''
    if value_type == 'str' and string != '':
        return string

    if value_type == 'int':
        for char in string:
            if char > '9' or char < '0':
                return None
        
        return int(string)
    
    if value_type == 'float':
        try:
            ans = float(string)
            return ans
        except Exception as e:
            print(e)
            return None
    
    return None

class Flag():
    flag_with_arg_ptn = re.compile(r'[\[, \(]-(?P<short_name>[^\[\]\(\)<>]*)\|--(?P<long_name>[^\[\]\(\)<>]*):(?P<value_type>[^\[\]\(\)<>]*)[\], \)]')
    flag_without_arg_ptn = re.compile(r'[\[, \(]-(?P<short_name>[^\[\]\(\)<>]*)\|--(?P<long_name>[^\[\]\(\)<>]*)[\], \)]')
    def __init__(self, short_name, long_name, value_type, is_compulsory):
        '''
        强制有值：--delete也可以设成有值的，虽然不推荐
        强制无值：--delete
        非强制有值：--max_int 10
        非强制无值：--keyword
        '''
        self.short_name = short_name 
        self.long_name = long_name
        self.value_type = value_type
        self.is_compulsory = is_compulsory
        if self.value_type:
            self.value = None
        else:
            self.value = False
    
    @classmethod
    def create_from_string(cls, string):
        '''
        [-g|--global]
        [-p|--prob: float] 
        
        查询时：
        (-q|--query)
        [-k|--keyword]
        这种无参数的flag可以直接-kq
        有参数的得按顺序，比如-ab x y 
        '''
        re.sub(r'\s+', '', string)
        res = cls.flag_with_arg_ptn.search(string)
        if res:
            res = res.groupdict()
            return cls(res['short_name'], res['long_name'], res['value_type'], (string[0] == '('))
        res = cls.flag_without_arg_ptn.search(string)
        if res:
            res = res.groupdict()
            return cls(res['short_name'], res['long_name'], None, (string[0] == '(')) 
        print("string=" + string)
        raise AssertionError("Flag cannot parse this string")
    def __str__(self):
        return '<Flag Object>: {}'.format(self.__dict__)
    def clear_value(self):
        if self.value_type is None:
            self.value = False
        else:
            self.value = None

class Arg():
    args_pattern = re.compile(r'<(?P<name>[^\[\]\(\)<>]*):(?P<value_type>[^\[\]\(\)<>]*)>')
    def __init__(self, name, value_type):
        self.name = name 
        self.value_type = value_type
        self.value = None
    
    @classmethod
    def create_from_string(cls, string):
        # print(string)
        re.sub(r'\s+', '', string)
        res = cls.args_pattern.search(string)
        if res:
            res = res.groupdict()
            return cls(res['name'], res['value_type'])
        raise AssertionError("Arg cannot parse this string")
    def __str__(self):
        return '<Arg Object>: {}'.format(self.__dict__)
    def clear_value(self):
        self.value = None
    
class ArgPattern:
    '''
    header + flags_no_arg_cpl + args + other_flags

    in other_flags: first, process no_arg flags, then pair remain flags and their values according to the order
    '''
    def __init__(self, name, pattern_str):
        '''
        A pattern of a command.
        
        args: <answer: str>

        '''
        self.name = name

        args, flags = self._split(pattern_str)
        self.args = args
        self.flags = flags
        self.flags_arg = [x for x in flags if x.value_type]
        self.flags_no_arg = [x for x in flags if x.value_type is None]
        self.flags_no_arg_cpl = [x for x in self.flags_no_arg if x.is_compulsory]
        self.flags_no_arg_not_cpl = [x for x in self.flags_no_arg if not x.is_compulsory]
        self.flags_arg_cpl = [x for x in self.flags_arg if x.is_compulsory]
        self.flags_arg_not_cpl = [x for x in self.flags_arg if not x.is_compulsory]


    def _split(self, pattern_str):
        '''
        split the pattern string into flags, then set self.optional_flags and compulsory_flags right.
        '''
        pattern_str = pattern_str.replace(' ', '')
        flags_pattern = re.compile(r'[\[, \(][^\[\]\(\)<>]*[\], \)]')
        args_pattern = re.compile(r'<[^\[\]\(\)<>]*>')
        
        # print(flags_pattern.findall(pattern_str))
        # print(args_pattern.findall(pattern_str))
        flags = [Flag.create_from_string(x) for x in flags_pattern.findall(pattern_str)]
        args = [Arg.create_from_string(x) for x in args_pattern.findall(pattern_str)]
        return args, flags
        
    def parse(self, string):
        result = None

        flags_long_dict = dict()
        flags_short_dict = dict()
        for f in self.flags:
            flags_long_dict[f.long_name] = f 
            flags_short_dict[f.short_name] = f
        
        segments = re.split(r' +', string.strip())
        current_status = 'flags_no_arg_cpl'
        total_num_flags_no_arg_cpl = len(self.flags_no_arg_cpl)
        current_num_flags_no_arg_cpl = 0
        current_flag = None 
        total_args_num = len(self.args)
        current_args_num = 0
        # ret = dict()
        pos = 0
        for seg in segments:
            pos += 1
            if current_status == 'flags_no_arg_cpl' and total_num_flags_no_arg_cpl == 0:
                current_status = 'args'
            if current_status == 'flags_no_arg_cpl':
                if seg[0] != '-':
                    self._clear()
                    return None
                if seg[:2] == '--':
                    try:
                        current_flag = flags_long_dict[seg[2:]]
                    except Exception as e:
                        print(e)
                        self._clear()
                        return None
                else:
                    for c in seg[1:]:
                        try:
                            current_flag = flags_short_dict[seg[1:]]
                            # print('detect {}'.format(seg[1:]))
                        except Exception as e:
                            print(e)
                            self._clear()
                            return None 
                current_flag.value = True
                current_num_flags_no_arg_cpl += 1
                if (current_num_flags_no_arg_cpl == total_num_flags_no_arg_cpl):
                    current_status = 'args'
                    continue

            if current_args_num == total_args_num:
                break
            if current_status == 'args':
                if total_args_num == 0:
                    break
                if seg[0] == '-':
                    self._clear()
                    return None 
                try:
                    self.args[current_args_num].value = parse_value(seg, self.args[current_args_num].value_type)
                    current_args_num += 1
                except Exception as e:
                    print(e)
                    self._clear()
                    return None
                if current_args_num == total_args_num:
                    break
        
        # remain: [pos:]
        if current_num_flags_no_arg_cpl != total_num_flags_no_arg_cpl:
            self._clear()
            return None
        if current_args_num != total_args_num:
            self._clear()
            return None 
        

        values = []
        for i in range(pos, len(segments)):
            seg = segments[i]
            if seg[0] != '-':
                values.append(segments[i])
                continue

            if seg[:2] == '--':
                if flags_long_dict[seg[2:]].value_type is None:
                    flags_long_dict[seg[2:]].value = True
                    segments[i] = ''
            else:

                for c in seg[1:]:
                    if flags_short_dict[c].value_type is None:
                        flags_short_dict[c].value = True
                        segments[i] = segments[i].replace(c, '') 

        value_pos = 0
        for seg in segments[pos:]:
            if seg[0] != '-':
                continue
            if seg[:2] == '--':
                _flag = flags_long_dict[seg[:2]]
                _flag.value = parse_value(values[value_pos], _flag.value_type)
                value_pos += 1
            else:
                for c in seg[1:]:
                    _flag = flags_short_dict[c]
                    _flag.value = parse_value(values[value_pos], _flag.value_type)
                    value_pos += 1
        
        ret = dict()
        for f in self.flags:
            ret[f.long_name] = f.value
        
        for a in self.args:
            ret[a.name] = a.value
        
        ret['name'] = self.name
        
        self._clear()
        return ret    


    def _clear(self):
        for f in self.flags:
            f.clear_value()
        for a in self.args:
            a.clear_value()

async def send_msg_with_delay(session:CommandSession, msg:str):
    if '\\w' not in msg:
        await session.send(msg)
        return 
    msg = msg.split('\\w')
    for m in msg[:-1]:
        await session.send(m)
        await asyncio.sleep(1.0)
    await session.send(m)
    return 

async def usr_group_send_msg_with_delay(user, group, msg):
    if group is not None:
        await send_group_msg_with_delay(group.group_id, msg)
        return 
    await send_usr_msg_with_delay(user.uesr_id, msg)
    

async def send_group_msg_with_delay(group_id:int, msg:str):
    if '$w' not in msg:
        await nonebot._bot.send_group_msg(group_id=group_id, message=msg)
        return 
    msg = msg.split('$w')
    for m in msg[:-1]:
        await nonebot._bot.send_group_msg(group_id=group_id, message=m)
        await asyncio.sleep(1.4)
    await nonebot._bot.send_group_msg(group_id=group_id, message=msg[-1])
    return

async def send_usr_msg_with_delay(user_id:int, msg:str):
    if '$w' not in msg:
        await nonebot._bot.send_private_msg(user_id=user_id, message=msg)
        return 
    msg = msg.split('$w')
    for m in msg[:-1]:
        await nonebot._bot.send_private_msg(user_id=user_id, message=m)
        await asyncio.sleep(1.4)
    await nonebot._bot.send_private_msg(user_id=user_id, message=msg[-1])
    return

def record_and_check_operation(user_id:int, operation:str, msg:str):
    # print('_____BLOCK_OFF_____:{}'.format(BLOCK_OFF))
    ts = time.time()
    # print("ts={}".format(ts))
    _current = {
            "operation": operation,
            "message": msg,
            "timestamp": ts
    }
    if str(user_id) in BLOCK_OFF:
        if ts - BLOCK_OFF[str(user_id)] > BLOCK_INTERV:
            del BLOCK_OFF[str(user_id)]
        else:
            return False

    if str(user_id) not in RECENT_OP:
        RECENT_OP[str(user_id)] = [_current]
        if str(user_id) in BLOCK_OFF:
            return False
        return True
    else:
        RECENT_OP[str(user_id)].append(_current)
    

    for index in range(len(RECENT_OP[str(user_id)]))[::-1]:
        record = RECENT_OP[str(user_id)][index]
        if ts - record["timestamp"] > RECORD_INTERV or ts < record["timestamp"]:
            del RECENT_OP[str(user_id)][index]

    
    cnt = 0
    for index in range(len(RECENT_OP[str(user_id)]))[::-1]:
        record = RECENT_OP[str(user_id)][index]
        if ts - record["timestamp"] < SHORT_INTERV:
            cnt += 1
    
    if str(user_id) in BLOCK_OFF:
        return False      
    
    if len(RECENT_OP[str(user_id)]) > MAX_LEN or cnt > SHORT_MAX_LEN:
        BLOCK_OFF[str(user_id)] = ts
        return False  
    
    _ = RECENT_OP[str(user_id)][-1]["message"]
    cnt = 0
    for r in RECENT_OP[str(user_id)][::-1]:
        if _ == r["message"]:
            cnt += 1
        else:
            break
    
    if cnt >= MAX_SAME_MSG:
        BLOCK_OFF[str(user_id)] = ts
        return False 

    _ = RECENT_OP[str(user_id)][-1]["operation"]
    cnt = 0
    for r in RECENT_OP[str(user_id)][::-1]:
        if _ == r["operation"]:
            cnt += 1
        else:
            break
    
    if cnt >= MAX_SAME_OP:
        BLOCK_OFF[str(user_id)] = ts
        return False 
    
    return True

def check_CD(user:User, operation:str):
    user_id = user.user_id
    if user_id in SUPERUSERS:
        return True
    ts = time.time()
    if operation not in CMD_CD:
        return True 
    if str(user_id) not in RECENT_OP:
        return True 
    for r in RECENT_OP[str(user_id)]:
        if r["operation"] == operation and (ts - r["timestamp"]) < CMD_CD[operation]:
            return False 
    return True

async def check_cd_times(user, group, cmd_name):
    if not await check_cmd_times(user, cmd_name):
        await nonebot._bot.send_group_msg(group_id=group.group_id, message=TIMES_UP_MSG)
        return False
    if not check_CD(user, cmd_name):
        await nonebot._bot.send_group_msg(group_id=group.group_id, message="该命令存在{}秒冷却时间，请稍后尝试x".format(CMD_CD[cmd_name]))
        return False
    if not record_and_check_operation(user.user_id, cmd_name, ""):
        return False
    return True

async def check_auth(user, group, auth_needed):
    if user.auth < auth_needed and group.auth < auth_needed and user.user_id not in SUPERUSERS:
        return False
    return True