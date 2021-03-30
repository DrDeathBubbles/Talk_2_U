import redis 
from tools.talkbot_sqs import sqs_queue

class redis_control_database:
    redis_schema = {'primary_key':'key',
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

    def safe_make_record(self,key, priority = 0):
        if self.check_exists_redis(key):
            return False 
        else:
            self.make_record(key, priority = priority)
            return True     


    def update_field(self, key, field, value):
        if self.check_exists_redis(key) and self.check_field_in_schema_fields(field):
            self.conn.hset(key,field,value)
            return True
        else:
            #logging.error(f'{key},{field} not available')
            print(f'{key},{field} not available')
            return False 


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
            type = conn.type(key)
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

 
        


class redis_data_queue(redis_control_database, sqs_queue):

    redis_schema = {'primary_key':'key',
    'title':'unset',
    'description':'unset',
    'vimeo_url':'unset',
    'priority':0
    }

    def __init_subclass__(cls):
        return super().__init_subclass__()


