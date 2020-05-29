from nonebot.default_config import * 
import os

SUPERUSERS = {}
ACCESS_TOKEN = ""
COMMAND_START = {'.', '/'}

DB_HOST = ''
DB_USER = ''
DB_PASSWORD = ''
DB_NAME = ''

# Akina settings
USER_DATAPATH = os.path.join('.', 'data', 'userdata')
ITEM_DATAPATH = os.path.join('.', 'data', 'items.json')

CALLME_AUTH = 1
ANSWER_AUTH = 1
WEATHER_AUTH = 1
TEACH_AUTH = 2
TEACH_ALREADY_EXISTS_MSG = "问答已存在"
LOTTERY_AUTH = 2
GROUP_AUTH = 3
ANNOUNCE_AUTH = 6
SYSTEM_AUTH = 5

COMMAND_TIMES = {
    'weather': 5,
    'teach': 10,
    'python': 10,
    'lottery': 10,
    'callme': 10,
    'kokeman': 15
}

ARGUMENT_ERROR_MSG = '参数错误'

CITY_JSON_PATH = os.path.join('.', 'plugins', 'weather', 'city.json')

NO_NICKNAME = '__NOT_DEFINED__'

LOTTERY_N_PROB = 0.5
LOTTERY_R_PROB = 0.3
LOTTERY_SR_PROB = 0.15
LOTTERY_SSR_PROB = 0.05


TIMES_CMD = ['lottery', 'teach', 'weather']

TIMES_UP_MSG = "调用次数已达上限."

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

CD_CMD = {
    "lottery": 120
}

GROUP_INFORMED = []