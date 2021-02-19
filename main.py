import logging
import boto3
import multiprocessing
from logging import handlers
from listener import listener_process
from worker import worker_process
from aws import get_object_url


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



    sqs = boto3.resource('sqs',region_name = 'eu-west-1')
    q = sqs.get_queue_by_name(QueueName='DS_AJM_VIDEO')  

   
    while True:
        messages = []
        rs = q.receive_messages()
        for m in rs:
            temp = json.loads(m.body)
            m.delete()
            try:
                temp = temp['Records'][0]['s3']['object']['key']
                temp = unquote(temp)
            except KeyError as ke:
                logging.error('A key error {} has occured while trying\
                to access the S3 filename.')
            messages.append(temp)

        for message in messages:
            print(message) 




if __name__ == '__main__':
    main()