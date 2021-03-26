from tools.talkbot_sqs import sqs_queue
from tools.talkbot_redis import redis_control_database
from tools.talkbot_s3 import s3_bucket
from vimeo.video_upload import v


def main(bucket = 'cc21-ouput', local_file_location = '/'):
    vimeo_queue = sqs.queue('talkbot_vimeo')
    r =
    bucket = s3_bucket(bucket) 
    while True:
        messages = vimeo_queue.get_sqs_message() 
        for message in messages:
            local_file = local_file_location + message
            data = r.get_talk_data(message)
            bucket.retrieve_from_s3(message, local_file)
            if data :
                vimeo_url = vimeo_upload(local_file, d['title'],d['description'])
            else:
                vimeo_url = vimeo_upload(local_file,'Unset','Unset','private')     
    
            r.update_field(self, message,'vimeo',vimeo_url)
