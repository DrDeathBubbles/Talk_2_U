import boto3
import json 


class sqs_queue:

    def __init__(self, queue_name):
        self.sqs = boto3.resource('sqs', region_name = 'eu-west-1')
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)

    def get_sqs_message(self,):
        out = []
        messages = self.queue.receive_messages()
        for m in messages:
            out.append(json.loads(m.body)
            m.delete()
        return out    
    
    def send_sqs_message(self, message):
        response = self.queue.send_message(MessageBody=message)