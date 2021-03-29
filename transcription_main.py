from tools.talkbot_redis import redis_control_database
from tools.talkbot_s3 import s3_bucket
from transcription.transcription import transcribe
#This needs to be investaged/updated 
from transcription.Transcription_control import generate_transcription_translate_import 


def main(redis_port = '6379', transcription_queue_name = 'talkbot_transcription',
local_file_location = '/', bucket_name = 'cc21-transcriptions'):
    transcription_queue = sqs.queue(transcription_queue_name)
    r = redis_control_database(redis_port)
    bucket = s3_bucket(bucket_name)
    while True:
        messages = transcription_queue.get_sqs_message() 
        for key in messages:
            data = r.get_data(key)
            texts = generate_transcription_translate_import(data['s3_raw'], file_location = './')
            for k, value in texts.items():
                bucket.post_to_s3(value)
                r.update_field(key, k, value)


            






