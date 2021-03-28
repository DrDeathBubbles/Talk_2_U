from tools.talkbot_redis import redis_control_database
from transcription.transcription import transcribe 


def main(redis_port = '6379', transcription_queue_name = 'talkbot_transcription',
local_file_location = '/'):
    transcription_queue = sqs.queue(transcription_queue_name)
    r = redis_control_database(redis_port)
    t = transcribe()
    while True:
        messages = transcription_queue.get_sqs_message() 
        for message in messages:
           t. 






            local_file = local_file_location + message
            data = r.get_talk_data(message)
            bucket.retrieve_from_s3(message, local_file)
            if data :
                vimeo_url = vimeo_upload(local_file, d['title'],d['description'])
            else:
                vimeo_url = vimeo_upload(local_file,'Unset','Unset','private')     
    
            r.update_field(self, message,'vimeo',vimeo_url)
    