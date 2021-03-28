from tools.talkbot_redis import redis_control_database
from tools.talkbot_sqs import sqs_queue
from tools.talkbot_redis import redis_control_database
from tools.tools import data_format_s3
from aws import get_object_url


def __main__(region,redis_port = 6379, input_queue = 'talkbot_s3'):
    r = redis_control_database(redis_port)
    s3_queue = sqs_queue(input_queue)

    talkbot_priority = sqs_queue('talkbot_priority')
    talkbot_normal = sqs_queue('talkbot_normal')
    talkbot_transcription = sqs_queue('talkbot_transcription')

    
    while True:
        messsages = s3_queue.get_sqs_message()
        for message in messages:
            key = data_format_s3(message)
            if r.check_exists(key):
                if r.get_field(key,'priority') == 0:
                    talkbot_normal.send_sqs_message(key)
                    talkbot_transcription.send_sqs_message(key)
                else:
                    talkbot_priority.send_sqs_message(key)
                    talkbot_transcription.send_sqs_message(key)    
            
            else:
                r.make_record(key)
                url = get_object_url(key)
                r.update_field(key,'s3_raw',url)
                talkbot_normal.send_sqs_message(key)
                talkbot_transcription.send_sqs_message(key)

            
if __name__ == '__main__':
    main()            
            
     






