import logging
import boto3
import multiprocessing
from logging import handlers
from tools.tools import data_format_s3
from tools.talkbot_sqs import sqs_queue
from tools.talkbot_redis import redis_control_database
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


def main(redis_port = 6379, free_cores = 0, num_priority = 1):
    listner_queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(
        target=listener_process, args=(listner_queue,))
    listener.start()
    root_configurer(listner_queue)


    talkbot_processing_priority =  sqs_queue('talkbot_processing_priority')
    talkbot_processing_normal = sqs_queue('talkbot_processing_normal')
    talkbot_vimeo = sqs_queue('talkbot_vimeo')

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
            formatted_data = data_format_s3(message)
            try:
                priority_task_queue.put(formatted_data)
            except:
               logger.error(f'Could not add {message} to priority queue')

        for message in normal_messages:
            formatted_data = data_format_s3(message) 
            try:
                normal_task_queue.put(formatted_data) 
            except:
                logger.error(f'Could not add {message} to normal queue')          






if __name__ == '__main__':
    main()