from nonebot.default_config import * 
import os

SUPERUSERS = {}
ACCESS_TOKEN = ""
COMMAND_START = {'#!', '秋菜酱，', '秋菜酱 '}

DB_HOST = ''
DB_USER = ''
DB_PASSWORD = ''
DB_NAME = ''


# Akina settings
USER_DATAPATH = os.path.join('.', 'data', 'userdata')
ITEM_DATAPATH = os.path.join('.', 'data', 'items.json')
CITY_JSON_PATH = os.path.join('.', 'plugins', 'weather', 'city.json')

# authority, CD and times
ANSWER_AUTH = 1
LOTTERY_AUTH = 2
ANNOUNCE_AUTH = 6

CMD_AUTH = {
    "weather": 1,
    "times": 1,
    "teach": 2,
    "system": 5,
    "lookup": 1,
    "group": 4,
    "greet": 1,
    "callme": 1,
    "asset": 2,
    "announce": 5,
    "lottery": 2
}

CMD_TIMES = {
    'weather': 5,
    'teach': 30,
    'python': 10,
    'lottery': 10,
    'callme': 10,
    'kokeman': 15
}

CMD_CD = {
    "lottery": 120
}


# nickname, lottery

NO_NICKNAME = '__NOT_DEFINED__'

LOTTERY_N_PROB = 0.5
LOTTERY_R_PROB = 0.3
LOTTERY_SR_PROB = 0.15
LOTTERY_SSR_PROB = 0.05


# block settings
RECENT_OP = {
    "user_id": []
}

RECORD_INTERV = 90
SHORT_INTERV = 13

MAX_LEN = 15
SHORT_MAX_LEN = 5

BLOCK_OFF = {
}
BLOCK_INTERV = 300
MAX_SAME_MSG = 4
MAX_SAME_OP = 7


# messages
IN_CD_MSG = "该命令存在{}秒冷却时间，请稍后尝试x"
LOW_AUTH_MSG = "权限不足."
TEACH_ALREADY_EXISTS_MSG = "问答已存在"
TIMES_UP_MSG = "调用次数已达上限."
ARGUMENT_ERROR_MSG = '参数错误'

GROUP_INFORMED = []