import redis 
from vimeo_tools.video_upload import * 

class redis_control_database:
    redis_schema = {'video_key':'unset',
    's3_raw':'unset',
    's3_processed':'unset',
    'transcript':'unset',
    'vimeo':'unset',
    'audio':'unset',
    'vtt':'unset',
    'srt':'unset',
    'priority':0
    }
    
    def __init__(self, port):
        self.port = port
        self.conn = redis.StrictRedis(host='localhost', port = port, db=0, decode_responses=True)

    def check_exists_redis(self, key):
        if self.conn.exists(key):
            return True
        else:
            return False       


    def check_field_in_schema_fields(self, field):
        if field in self.redis_schema.keys():
            return True
        else:
            return False     

    def make_record(self, key, priority = 0):
        schema = self.redis_schema.copy()
        schema['primary_key'] = key
        schema['priority'] = priority
        self.conn.hmset(key, schema)

    def make_record_from_dict(self, key, data = {}):
        schema = self.redis_schema.copy()
        for k, d in data.items():
            if self.check_field_in_schema_fields(k):
                schema[k] = d
            else:
                print(f'{k} not in schema')
        self.conn.hmset(key, schema)        


    def safe_make_record(self,key, priority = 0):
        if self.check_exists_redis(key):
            return False 
        else:
            self.make_record(key, priority = priority)
            return True

    def safe_make_record_from_dict(self, key, data = {}):
        if self.check_exists_redis(key):
            return False            
        else:
            self.make_record_from_dict(key, data)
            return True



    def update_field(self, key, field, value):
        if self.check_exists_redis(key) and self.check_field_in_schema_fields(field):
            self.conn.hset(key,field,value)
            return True
        else:
            #logging.error(f'{key},{field} not available')
            print(f'{key},{field} not available')
            return False 

    def update_dict(self, key, data):
        schema = self.redis_schema.copy()
        if self.check_exists_redis(key):
            for k, d in data.items():
                if self.check_field_in_schema_fields(k):
                    schema[k] = d
        self.conn.hmset(key, schema)                    

    def update_or_create(self, key, data):
        if self.safe_make_record_from_dict(key, data):
            return
        else:
            self.update_dict(key, data) 


    def get_field(self, key, field):
        if self.check_exists_redis(key) and self.check_field_in_schema_fields(field):
            data = self.conn.hget(key,field)
        else:
            #logging.error(f'{key},{field} not available')
            print(f'{key},{field} not available')
            data = {}
        return data

    def get_data(self, key):
        if self.check_exists_redis(key): 
            data = self.conn.hgetall(key)
        else:
            #logging.error(f'{key} does not exist in redis')
            print(f'{key} does not exist in redis')    
            data = {}
        return data

    def get_all_data(self, ):
        keys = self.conn.keys('*')
        out = []
        for key in keys:
            type = self.conn.type(key)
            if type == "string":
                out.append(self.conn.get(key))
            if type == "hash":
                out.append(self.conn.hgetall(key))
            if type == "zset":
                out.append(self.conn.zrange(key, 0, -1))
            if type == "list":
                out.append(self.conn.lrange(key, 0, -1))
            if type == "set":
                out.append(self.conn.smembers(key))
        return out        

 
        


class redis_talk_database(redis_control_database):

    redis_schema = {'talk_key':'unset',
    'video_key':'unset',
    'title':'unset',
    'description':'unset',
    's3_processed':'uset',
    'vimeo':'unset',
    }

    def __init__(self,port):
        super().__init__(port)
        self.conn = redis.StrictRedis(host='localhost', port = port, db=1, decode_responses=True) 
        

    def make_record(self, key):
        schema = self.redis_schema.copy()
        schema['primary_key'] = key
        self.conn.hmset(key, schema)

                

    def make_record_details(self, key, title, description):
        schema = self.redis_schema.copy()   
        schema['primary_key'] = key
        schema['title'] = title
        schema['description'] = description
        self.conn.hmset(key, schema) 

    def safe_make_record(self, key, priority=0):
        if self.check_exists_redis(key):
            return False 
        else:
            self.make_record(key)
            return True


    def brute_insert_data(self, key, title, description):
        self.update_field(key, 'title', title)
        self.update_field(key,'description', description)

    def insert_data(self, key, title, description):
        if self.check_exists_redis(key):
            title_change = self.get_field(key, 'title') != title
            description_change = self.get_field(key,'description') != description
            if title_change: 
                self.update_field(key, 'title', title)
            if description_change:
                self.update_field(key,'description', description)
            if title_change or description_change:
                vimeo_url = self.get_field(key, 'vimeo') 
                if vimeo_url != 'unset': 
                    vimeo_id = vimeo_id(self.get_field(key, 'vimeo'))
                    update_title_description(id_vimeo, title, description)
        else:
            self.make_record_details(key, title, description)       
