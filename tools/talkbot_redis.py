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

    def check_exsits_redis(self, key):
        if self.conn.exists(key):
            return True
        else:
            return False       


    def check_field_in_schema_fields(self, field):
        if field in self.redis_schema.keys():
            return True
        else:
            return False     

    def make_record(self, key):
        schema = self.redis_schema.copy()
        schema['primary_key'] = key
        self.conn.hmset(key, schema)

    def update_field(self, key, field, value):
        if self.check_exits_redis(key) and self.check_field_in_schema_fields(field):
            self.conn.hmset(key,field,value)
        else:
            #logging.error(f'{key},{field} not available')
            print(f'{key},{field} not available')


    def get_field(self, key, field):
        if self.check_exits_redis(key) and self.check_field_in_schema_fields(field):
            data = self.conn.hget(key,field)
        else:
            #logging.error(f'{key},{field} not available')
            print(f'{key},{field} not available')
            data = {}
        return data

    def get_data(self, key):
        if self.check_exsits_redis(key): 'Field not in schema'
            data = self.conn.hgetall(key)
        else:
            #logging.error(f'{key} does not exist in redis')
            print(f'{key} does not exist in redis')    
            data = {}
        return data


 
        


class redis_data_queue(redis_control_database, sqs_queue):

    def __init_subclass__(cls):
        return super().__init_subclass__()