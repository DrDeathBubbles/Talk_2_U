from tools.talkbot_sqs import sqs_queue
from tools.talkbot_redis import redis_control_database, redis_talk_data
from tools.talkbot_s3 import s3_bucket
from vimeo.video_upload import vimeo_upload


def main(bucket = 'cc21-ouput', local_file_location = '/', port = ''6378):
    vimeo_queue = sqs.queue('talkbot_vimeo')
    talk_data = redis_talk_data(port)
    video_data = redis_control_database(port) 
    bucket = s3_bucket(bucket) 
    while True:
        messages = vimeo_queue.get_sqs_message() 
        for message in messages:
            local_file = local_file_location + message
            data = r.get_talk_data(message)
            bucket.retrieve_from_s3(message, local_file)
            if data.check_exists_redis():
                d = data.get_data(message)
                vimeo_url = vimeo_upload(local_file, d['title'],d['description'])
            else:
                vimeo_url = vimeo_upload(local_file,'Unset','Unset','private')     
    
            video_data.update_field(message,'vimeo',vimeo_url)
            talk_data.update(message, 'vimeo', vimeo_url)
