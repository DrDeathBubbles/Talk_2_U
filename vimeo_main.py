from tools.talkbot_sqs import sqs_queue
from tools.talkbot_redis import redis_control_database, redis_talk_data
from tools.talkbot_s3 import s3_bucket
from vimeo_tools.video_upload import vimeo_upload


def main(bucket = 'cc21-ouput', local_file_location = '/', port = '6378', queue ='talkbot_vimeo'):
    vimeo_queue = sqs_queue(queue)
    talk_data = redis_talk_data(port)
    video_data = redis_control_database(port) 
    bucket = s3_bucket(bucket) 
    while True:
        messages = vimeo_queue.get_sqs_message_raw() 
        for message in messages:
            local_file = local_file_location + message
            bucket.retrieve_from_s3(message, local_file)
            if data.check_exists_redis(message):
                d = data.get_data(message)
                vimeo_url = vimeo_upload(local_file, d['title'],d['description'])
            else:
                vimeo_url = vimeo_upload(local_file,'Unset','Unset','private')     
    
            video_data.update_field(message,'vimeo',vimeo_url)
            talk_data.update(message, 'vimeo', vimeo_url)


if __name__ == '__main__':
    main()