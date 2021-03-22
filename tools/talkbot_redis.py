import redis 

class redis_control_database:
    redis_schema = {'primary_key':'key',
    's3_raw':'unset',
    's3_processed':'unset',
    'transcript':'unset',
    'vimeo':'unset',
    'audio':'unset',
    'priority':0
    }
    
    def __init__(self, port):
        self.port = port
        self.conn = redis.StrictRedis(host='localhost', port = port, db=0, decode_responses=True)

    def check_keys_in_redis_fields(self, field):
        if field in redis_schema.keys():
            return True
        else:
            return False     

    def make_record(self, key):
        schema = self.redis_schema.copy()
        schema['primary_key'] = key
        self.conn.hset(key, schema)

    def update_field(self, key,field,value):
        assert self.check_keys_in_redis_fields(field), 'Field not in schema'
        self.conn.hset(key,field,value)

    def get_field(self, key,field,value):
        assert self.check_keys_in_redis_fields(field), 'Field not in schema'
        data = self.conn.hget(key,field)
        return data

    def check_exits(self, key):
        if self.conn.exists(key):
            return True
        else:
            return False        
        


