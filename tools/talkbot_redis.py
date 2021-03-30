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

    def check_keys_in_redis_fields(self, field):
        if field in self.redis_schema.keys():
            return True
        else:
            return False     

    def make_record(self, key):
        schema = self.redis_schema.copy()
        schema['primary_key'] = key
        self.conn.hmset(key, schema)

    def update_field(self, key,field,value):
        assert self.check_keys_in_redis_fields(field), 'Field not in schema'
        self.conn.hmset(key,field,value)

    def get_field(self, key,field):
        assert self.check_keys_in_redis_fields(field), 'Field not in schema'
        data = self.conn.hget(key,field)
        return data

    def get_data(self, key):
        assert self.check_keys_in_redis_fields(field), 'Field not in schema'
        data = self.conn.hgetall(key)
        return data


    def check_exits(self, key):
        if self.conn.exists(key):
            return True
        else:
            return False        
        


class redis_data_queue(redis_control_database, sqs_queue):

    def __init_subclass__(cls):
        return super().__init_subclass__()