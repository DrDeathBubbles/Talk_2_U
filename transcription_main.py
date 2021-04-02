from tools.talkbot_redis import redis_control_database, redis_talk_database
from tools.talkbot_s3 import s3_bucket
from tools.talkbot_sqs import sqs_queue
import sys
import os
sys.path.append(os.path.abspath('../talkbot_transcription/source/'))
#This needs to be investaged/updated 
from Transcription_control import generate_transcription_translate_import 


def main(redis_port = '6378', transcription_queue_name = 'talkbot_transcription',
local_file_location = './', bucket_name = 'cc21-ed'):
    transcription_queue = sqs_queue(transcription_queue_name)
    talk_data = redis_talk_database(redis_port)
    video_data = redis_control_database(redis_port) 
    bucket = s3_bucket(bucket_name)
    while True:
        messages = transcription_queue.get_sqs_message_raw() 
        for key in messages:
            text = generate_transcription_translate_import(key, languages = ['pt','es','de','fr'],
            process = 'cc21', translate = False, region ='eu-west-1', inbucket = 'cc21-raw', 
            file_location = local_file_location)
            for k, value in text.items():
                url = bucket.post_to_s3(value)
                video_data.update_field(key, k, url)
                




if __name__ == '__main__':
    main()            






