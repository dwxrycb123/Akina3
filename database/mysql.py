import asyncio 
import aiomysql 
import logging 

import os

class Database():
    def  __init__(self, host, user, password, database,
                 port=3306, charset='utf8', autocommit=True, maxsize=10, minsize=1):
        self.host = host
        self.user = user 
        self.password = password 
        self.database = database 
        self.port = port 
        self.charset = charset 
        self.autocommit = autocommit 
        self.maxsize = maxsize 
        self.minsize = minsize 
        
    
    def set_loop(self, loop):
        self.loop = loop
    
    async def create_pool(self):
        logging.info('creating database connection pool...')
        self.pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            charset=self.charset,
            autocommit=self.autocommit,
            maxsize=self.maxsize,
            minsize=self.minsize,
            loop=self.loop
        )
    
    async def select(self, sql, args, size=None):
        logging.info(sql + ':' +  str(args))
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args or ())
                if size:
                    rs = await cur.fetchmany(size)
                else:
                    rs = await cur.fetchall()
            logging.info('rows returned: {}'.format(len(rs)))
            return rs 
    
    async def execute(self, sql, args=None):
        logging.info(sql + ':' + str(args))
        async with self.pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    if args:
                        await cur.execute(sql.replace('?', '%s'), args)
                    else:
                        await cur.execute(sql.replace('?', '%s'))
                    affected = cur.rowcount
                    print('affected:{}'.format(affected))
                    r = await cur.fetchall()
                    print(r)
            except BaseException as e:
                raise e
            return r
    
    async def close_pool(self):
        logging.info('close database connection pool...')
        self.pool.close()
        await self.pool.wait_closed()

class Table():
    def __init__(self, database, table_name):
        self.attr = dict()
        self.database = database 
        self.table_name = table_name
        self.keys = []
        self.primary_key = None 

    def set_keys(self, keys, primary_key):
        """
        keys: a list of dicts, dicts has two attrs (name and dtype)
        primary: a dict with two attrs name and dtype
        """
        self.keys = list(keys)
        self.primary_key = primary_key
        self.key_names = [k['name'] for k in self.keys]

    def _fields_to_string(self):
        r = ['{} {}'.format(k['name'], k['dtype']) for k in self.keys]
        return ','.join(r) + ',' + 'PRIMARY KEY({})'.format(self.primary_key['name']) 
    
    def _tuple_to_dict(self, t, key_names_list):
        """
        convert a record from a tuple to a dict
        """
        res = {}
        for i in range(len(t)):
            res[key_names_list[i]] = t[i]
        return res

    def _tuples_to_dicts(self, ts, key_names_list):
        """
        convert records from a tuple of tuples to a list of dicts
        """
        res = []
        if key_names_list == ['*']:
            key_names_list = [k['name'] for k in self.keys]
        
        for i in range(len(ts)):
            res.append(self._tuple_to_dict(ts[i], key_names_list))
        return res 
    
    async def create(self):
        """
        create an empty table
        """
        # execute
        print('create TABLE IF NOT EXISTS {}({}) '.format(self.table_name, self._fields_to_string()))
        r = await self.database.execute('create TABLE IF NOT EXISTS {}({}) '.format(self.table_name, self._fields_to_string()))

        return r
    
    async def add_key(self, key):
        """
        add a new key into the table
        """
        self.keys.append(key)
        # alter table id_name add age int,add address varchar(11);
        r = await self.database.execute('alter table {} add {} {};'.format(self.table_name, key['name'], key['dtype']))

        return r
    
    async def delete_key(self, key):
        """
        delete a field of the table 
        """
        raise NotImplementedError
    
    async def select_record(self, conditions, key_names_list=['*'], args=None):
        """
        conditions: a dict like {'sex': 'male', 'age': 17} or a string
        dict will be converted into a string like 'where sex='male' and age=17"
        search for certain records
        return a dict/ dicts
        """
        if isinstance(conditions, dict):
            cond_str = []
            args = []
            for k, v in conditions.items():
                cond_str.append("{}=?".format(k))
                args.append(v)
            cond_str = ' AND '.join(cond_str)
            args = tuple(args)
        
        if isinstance(conditions, str):
            cond_str = conditions
        r = await self.database.execute('select {} from {} where {}'.format(','.join(key_names_list), self.table_name, cond_str), args)
        return self._tuples_to_dicts(r, key_names_list)
    
    async def add_record(self, record):
        keys_str = []
        values = []
        for k, v in record.items():
            keys_str.append(str(k))
            values.append(v)
        
        keys_str = ','.join(keys_str)
        num_args = len(values)
        values = tuple(values)

        # print('insert into {} ({}) VALUES ({})'.format(self.table_name, keys_str, ','.join(['?'] * num_args)))
        # print(values)
        r = await self.database.execute('insert into {} ({}) VALUES ({})'.format(self.table_name, keys_str, ','.join(['?'] * num_args)), values)
        return r
    
    async def delete_record(self, conditions, args=None):
        if isinstance(conditions, dict):
            cond_str = []
            args = []
            for k, v in conditions.items():
                cond_str.append("{}=?".format(k))
                args.append(v)
            cond_str = ' AND '.join(cond_str)
            args = tuple(args)
        
        if isinstance(conditions, str):
            cond_str = conditions
        print('delete from {} where {}'.format(self.table_name, cond_str))
        print(args)
        r = await self.database.execute('delete from {} where {}'.format(self.table_name, cond_str), args)
        return r

    
    async def update_record(self, content, conditions, args=None):
        args = []

        if isinstance(content, dict):
            cont_str = []
            for k, v in content.items():
                cont_str.append("{}=?".format(k))
                args.append(v)
            cont_str = ' , '.join(cont_str)

        if isinstance(content, str):
            cont_str = content
        
        if isinstance(conditions, dict):
            cond_str = []
            for k, v in conditions.items():
                cond_str.append("{}=?".format(k))
                args.append(v)
            cond_str = ' and '.join(cond_str)
        
        if isinstance(conditions, str):
            cond_str = conditions

        args = tuple(args)   
        print('update {} set {} where {}'.format(self.table_name, cont_str, cond_str))     
        await self.database.execute('update {} set {} where {}'.format(self.table_name, cont_str, cond_str), args)
    
    async def add_many(self, records):
        raise NotImplementedError

