import logging
import boto3
import multiprocessing
from logging import handlers
from tools.tools import data_format_s3
from tools.talkbot_sqs import sqs_queue
from tools.talkbot_redis import redis_control_database
from tools.talkbot_s3 import s3_bucket 
from listener import listener_process
from worker import video_processing



try:
    from urllib.parse import unquote 
except ImportError:
     from urlparse import unquote


logger = logging.getLogger(__name__)  # use module name


def root_configurer(queue):
    h = handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.ERROR)


def main(redis_port = 6379, free_cores = 0, num_priority = 1, input_bucket = 'cc21-raw'):
    listner_queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(
        target=listener_process, args=(listner_queue,))
    listener.start()
    root_configurer(listner_queue)


    talkbot_processing_priority =  sqs_queue('talkbot_processing_priority')
    talkbot_processing_normal = sqs_queue('talkbot_processing_normal')
    talkbot_vimeo = sqs_queue('talkbot_vimeo')

    bucket = s3_bucket(input_bucket)

    redis_main =  redis_control_database(redis_port)
    normal_task_queue = multiprocessing.Queue(-1)
    priority_task_queue = multiprocessing.Queue(-1)

    normal_tasks = []
    priority_tasks = []
    num_normal = multiprocessing.cpu_count() - free_cores - num_priority


    
    for i in range(num_normal):
        worker = multiprocessing.Process(target= video_processing,args=(listner_queue, normal_task_queue,
        redis_main, talkbot_vimeo))
        normal_tasks.append(worker)
        worker.start()
        
    for i in range(num_priority):
        worker = multiprocessing.Process(target= video_processing, args=(listner_queue, priority_task_queue,
        redis_main, talkbot_vimeo))
        priority_tasks.append(worker)
        worker.start()





    while True:
        priority_messages = talkbot_processing_priority.get_sqs_message()
        normal_messages = talkbot_processing_normal.get_sqs_message()
        for message in priority_messages:
            key = data_format_s3(message)
            if redis_main.safe_make_record(key):
                redis_main.update_field(key, 's3_raw', bucket.get_object_url(key))
            else:
                pass 

            try:
                priority_task_queue.put(key)
            except:
               logger.error(f'Could not add {key} to priority queue')

        for message in normal_messages:
            key = data_format_s3(message)
            if redis_main.safe_make_record(key):
                redis_main.update_field(key, 's3_raw', bucket.get_object_url(key))
            try:
                normal_task_queue.put(key) 
            except:
                logger.error(f'Could not add {key} to normal queue')          






if __name__ == '__main__':
    main(redis_port = '6378')