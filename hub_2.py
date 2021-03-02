from Talkbot_redis import redis_control_database
from Talkbot_sqs import sqs_queue, data_format_s3
from talkbot_redis import redis_control_database
from aws import get_object_url


def __main__(region, input_queue):
    r = redis_control_database(6379)
    s3_queue = sqs_queue('DS_AJM_VIDEO')

    talkbot_priority = sqs_queue('talkbot_priority')
    talkbot_normal = sqs_queue('talkbot_normal')

    
    while True:
        messsages = s3_queue.get_sqs_message()
        for message in messages:
            key = data_format_s3(message)
            url = get_object_url(key)
            r.make_record(key)
            r.update_field(key,'s3_raw',url)
            
            if r.get_field(key,'priority'):
                talkbot_priority.send_sqs_message()
            else:
                talkbot_normal.send_sqs_message()    






