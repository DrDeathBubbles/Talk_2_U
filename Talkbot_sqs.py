import boto3


class sqs_queue:

    def __init__(self, queue_name):
        self.sqs = boto3.resource('sqs', region_name = 'eu-west-1')
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)

    def send_sqs_message(message):
        response = self.queue.send_message(MessageBody=message)