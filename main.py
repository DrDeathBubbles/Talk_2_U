import logging
import boto3
import multiprocessing
from logging import handlers
from tools import monitor_queue, data_format_s3
from talkbot_sqs import sqs_queue
from listener import listener_process
from worker import worker_process
from aws import get_object_url


try:
    from urllib.parse import unquote 
except ImportError:
     from urlparse import unquote


logger = logging.getLogger(__name__)  # use module name


def root_configurer(queue):
    h = handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.DEBUG)


def main():
    listner_queue = multiprocessing.Queue(-1)
    listener = multiprocessing.Process(
        target=listener_process, args=(listner_queue,))
    listener.start()
    root_configurer(listner_queue)


    normal_task_queue = multiprocessing.Queue(-1)
    priority_task_queue = multiprocessing.Queue(-1)

    normal_tasks = []
    priority_tass = []
    num_normal = multiprocessing.cpu_count() - free_cores - num_priority

    
    for i in range(num_normal):
        worker = multiprocessing.Process(target=worker_process, args=(listner_queue,normal_task_queue))
        normal_tasks.append(worker)
        worker.start()
        
    for i in range(num_normal):
        worker = multiprocessing.Process(target=worker_process, args=(listner_queue,priority_task_queue))
        priority_tasks.append(worker)
        worker.start()


    sqs_priority =  sqs_queue('talkbot_priority')
    sqs_normal = sqs_queue('talkbot_normal')

    while True:
        monitor_queue(sqs_normal,data_format_s3,sqs_normal.put)
        monitor_queue(sqs_priority,data_format_s3,sqs_normal.put)
   



if __name__ == '__main__':
    main()