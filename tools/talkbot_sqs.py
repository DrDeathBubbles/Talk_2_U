import boto3
import json 


class sqs_queue:
    s3_sqs_message_format = {  
           "Records":[  
              {  
                 "eventVersion":"2.2",
                 "eventSource":"aws:s3",
                 "awsRegion":"us-west-2",
                 "eventTime":"The time, in ISO-8601 format, for example, 1970-01-01T00:00:00.000Z, when Amazon S3 finished processing the request",
                 "eventName":"event-type",
                 "userIdentity":{  
                    "principalId":"Amazon-customer-ID-of-the-user-who-caused-the-event"
                 },
                 "requestParameters":{  
                    "sourceIPAddress":"ip-address-where-request-came-from"
                 },
                 "responseElements":{  
                    "x-amz-request-id":"Amazon S3 generated request ID",
                    "x-amz-id-2":"Amazon S3 host that processed the request"
                 },
                 "s3":{  
                    "s3SchemaVersion":"1.0",
                    "configurationId":"ID found in the bucket notification configuration",
                    "bucket":{  
                       "name":"bucket-name",
                       "ownerIdentity":{  
                          "principalId":"Amazon-customer-ID-of-the-bucket-owner"
                       },
                       "arn":"bucket-ARN"
                    },
                    "object":{  
                       "key":"object-key",
                       "size":"object-size",
                       "eTag":"object eTag",
                       "versionId":"object version if bucket is versioning-enabled, otherwise null",
                       "sequencer": "a string representation of a hexadecimal value used to determine event sequence, only used with PUTs and DELETEs"
                    }
                 },
                 "glacierEventData": {
                    "restoreEventData": {
                       "lifecycleRestorationExpiryTime": "The time, in ISO-8601 format, for example, 1970-01-01T00:00:00.000Z, of Restore Expiry",
                       "lifecycleRestoreStorageClass": "Source storage class for restore"
                    }
                 }
              }
           ]
        }

    def __init__(self, queue_name):
        self.sqs = boto3.resource('sqs', region_name = 'eu-west-1')
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)

    def get_sqs_message(self,):
        out = []
        messages = self.queue.receive_messages()
        for m in messages:
            out.append(json.loads(m.body))
            m.delete()
        return out    
    
    def send_sqs_message(self, message):
        response = self.queue.send_message(MessageBody=message)
        return response 

    def send_s3_sqs_message(self,key):
        message = self.s3_sqs_message_format.copy()
        message['Records'][0]['s3']['object']['key'] = key
        self.send_sqs_message(message)