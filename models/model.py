from database.mysql import *

class User():
    # table_basic_info = 
    # ID, user_id, auth, nickname, property
    def __init__(self):
        self.__basic_data__ = dict()
        self.__command_times__ = dict()


    async def getUser(self, user_id):
        r = await self.table_basic_info.select_record({
            'user_id': user_id 
        })
        r_cmd = await self.table_command_times.select_record({
            'user_id': user_id
        })
        if len(r):
            self.__basic_data__ = r[0]
            self.__command_times__ = r_cmd[0]
        else:
            await self.table_basic_info.add_record({
                'user_id': user_id,
            })# 其余利用默认值
            await self.table_command_times.add_record({
                'user_id': user_id
            })# 每个命令的最大次数，命令的最大次数和所有命令的名称需要再config.py中注册；这里的话我们建立table的时候就设置好默认值，就可以插入空数据了
        # check if is in the database, if not: add_into_database
            r = await self.table_basic_info.select_record({
                'user_id': user_id 
            })
            r_cmd = await self.table_command_times.select_record({
                'user_id': user_id
            })
            self.__basic_data__ = r[0]
            self.__command_times__ = r_cmd[0]
        
        return self

    @classmethod
    def set_config(cls, db, table_basic_info, table_command_times):
        cls.db = db
        cls.table_basic_info = table_basic_info
        cls.table_command_times = table_command_times 
    
    def __getattr__(self, attr):
        # search in db
        if attr in self.__basic_data__:
            return self.__basic_data__[attr]
        
        if attr in self.__command_times__:
            return self.__command_times__[attr]
        
        raise AttributeError
    
    async def set(self, attr, value):
        # update in db
        print('set attr {}:{}'.format(attr, value))
        print('user_id:{}'.format(self.user_id))
        if attr in self.table_basic_info.key_names:
            await self.table_basic_info.update_record({
                attr: value
            }, 
            {
                'user_id': self.user_id
            })
            self.__basic_data__[attr] = value
            return
        
        if attr in self.table_command_times.key_names:
            await self.table_command_times.update_record({
                attr: value
            },
            {
                'user_id': self.user_id
            })
            self.__command_times__[attr] = value
            return
        
        raise AttributeError

# 问答不需要，问答的相关参数可以转化为sql的condition

class Group():
    # table_basic_info = 
    # ID, user_id, auth, nickname, property
    def __init__(self):
        self.__data__ = dict()
    
    async def getGroup(self, group_id):
        r = await self.table.select_record({
            'group_id': group_id 
        })
        if len(r):
            self.__data__ = r[0]
        else:
            await self.table.add_record({
                'group_id': group_id,
            })
            r = await self.table.select_record({
                'group_id': group_id 
            })
            self.__data__ = r[0]
        return self
    
    @classmethod
    def set_config(cls, db, table):
        cls.db = db
        cls.table = table
    
    def __getattr__(self, attr):
        # search in db
        if attr in self.__data__:
            return self.__data__[attr]
        
        raise AttributeError
    
    async def set(self, attr, value):
        # update in db
        if attr in self.table.key_names:
            await self.table.update_record({
                attr: value
            },
            {
                'group_id' : self.group_id
            })
            self.__data__[attr] = value
            return
        raise AttributeError

class Command():
    # 快乐复制粘贴
    # 除了调用次数 table_user_cmd_times
    pass 

# 这个很久后才可能更新了
class Kokeman():
    # kokeman_species
    # kokeman_user
    pass 

