from database.mysql import *
import time
from config import *

testdb = Database(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

# teach
teach_id = {
    'name': 'id',
    'dtype' : 'INT UNSIGNED NOT NULL AUTO_INCREMENT'
}

teach_question = {
    'name': 'question',
    'dtype' : 'VARCHAR(1000) character set utf8 NOT NULL'
}

teach_answer = {
    'name': 'answer',
    'dtype' : 'VARCHAR(1000) character set utf8 NOT NULL'
}

teach_prob = {
    'name': 'prob',
    'dtype': 'VARCHAR(40) NOT NULL DEFAULT "1.0"'
}

teach_env = {
    'name': 'env',
    'dtype': 'VARCHAR(1000) NOT NULL'
}

teach_date = {
    'name': 'create_date',
    'dtype' : 'VARCHAR(20) NOT NULL'
}

teach_author_id = {
    'name': 'author_id',
    'dtype' : 'BIGINT DEFAULT 0'
}

keys_teach = [teach_id, teach_question, teach_answer, teach_prob, teach_env, teach_date, teach_author_id]
table_teach = Table(testdb, 'teach_info')
table_teach.set_keys(keys_teach, teach_id)

# question_info
question_info_question_id = {
    'name': 'id',
    'dtype' : 'INT UNSIGNED NOT NULL AUTO_INCREMENT'
}

question_info_question = {
    'name': 'question',
    'dtype' : 'VARCHAR(1000) character set utf8 NOT NULL'
}

question_info_prob = {
    'name': 'prob',
    'dtype': 'VARCHAR(40) NOT NULL DEFAULT "1.0"'
}

quetion_info_env = {
    'name': 'env',
    'dtype': 'VARCHAR(1000) NOT NULL'
}

keys_question_info = [question_info_question_id, question_info_question, question_info_prob, quetion_info_env]
table_question_info = Table(testdb, 'question_info')
table_question_info.set_keys(keys_question_info, question_info_question_id)

# user_info
user_info_user_id = {
    'name': 'user_id',
    'dtype' : 'BIGINT NOT NULL'
}

user_info_auth = {
    'name': 'auth',
    'dtype': 'INT DEFAULT 1'
}

user_info_nickname = {
    'name': 'nickname',
    'dtype': 'VARCHAR(20) character set utf8 NOT NULL DEFAULT "__NOT_DEFINED__"'
}

user_info_property = {
    'name': 'property',
    'dtype': 'INT NOT NULL DEFAULT 10'
}

keys_user_info = [user_info_user_id, user_info_auth, user_info_nickname, user_info_property]
table_user_info = Table(testdb, 'user_info')
table_user_info.set_keys(keys_user_info, user_info_user_id)

# user_command_times
user_command_times_user_id = {
    'name': 'user_id',
    'dtype' : 'BIGINT NOT NULL'
}
user_command_times_weather = {
    'name': 'weather',
    'dtype' : 'INT NOT NULL DEFAULT 5'
}

user_command_times_teach = {
    'name': 'teach',
    'dtype' : 'INT NOT NULL DEFAULT 10'
}

user_command_times_python = {
    'name': 'python',
    'dtype' : 'INT NOT NULL DEFAULT 10'
}

user_command_times_lottery = {
    'name': 'lottery',
    'dtype' : 'INT NOT NULL DEFAULT 10'
}

user_command_times_callme = {
    'name': 'callme',
    'dtype' : 'INT NOT NULL DEFAULT 10'
}

user_command_times_kokeman = {
    'name': 'kokeman',
    'dtype' : 'INT NOT NULL DEFAULT 10'
}

# 少个callme 试试之后加

keys_user_command_times = [user_command_times_user_id, user_command_times_weather, user_command_times_teach, user_command_times_python, user_command_times_lottery, user_command_times_callme, user_command_times_kokeman]
table_user_command_times = Table(testdb, 'user_command_times')
table_user_command_times.set_keys(keys_user_command_times, user_command_times_user_id)

# 试着插入kokeman，确认插入列的功能可用；如何过0点清空还是问题

# group_info
group_info_group_id = {
    'name': 'group_id',
    'dtype' : 'BIGINT NOT NULL'
}

group_info_auth = {
    'name': 'auth',
    'dtype': 'INT NOT NULL DEFAULT 1'
}

keys_group_info = [group_info_group_id, group_info_auth]
table_group_info = Table(testdb, 'group_info')
table_group_info.set_keys(keys_group_info, group_info_group_id)
