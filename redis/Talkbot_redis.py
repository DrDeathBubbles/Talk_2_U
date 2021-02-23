import redis 

class redis_control_database:
    redis_schema = {'primary_key':key,
    's3_raw':'unset',
    's3_processed':'unset',
    'transcript':'unset',
    'vimeo':'unset',
    'audio':'unset',
    }
    
    def __init__(self, port):
        self.port = port
        self.conn = redis.Redis(host='localhost', port = port, db=0, decode_responses=True)

    def check_keys_in_redis_fields(field):
        if field in redis_schema.keys():
            return True
        else:
            return False     

    def make_record(key):
        self.connection.hmset(key, redis_schema)

    def update_field(key,field,value):
        assert self.check_keys_in_redis_fields(field), 'Field not in schema'
        self.connection.hset(key,field,value)

        


