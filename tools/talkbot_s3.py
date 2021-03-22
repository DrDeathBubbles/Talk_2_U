import botocore.session
import boto3
session = botocore.session.get_session()
s3 = session.create_client('s3')
s3._client_config.signature_version = botocore.UNSIGNED

sqs = boto3.resource('sqs')



class s3_bucket():

    def __init__(self, bucket_name):
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket_name
        self.bucket =  self.s3.Bucket(bucket_name) 


    def retrieve_from_s3(key, local_file):
        out = self.bucket.download_file(key, local_filename)
        return out

    def post_to_s3(local_file, key):
        out = self.bucket.upload_file(local_file, key)
        url = self.get_object_url(key)
        return url

    def get_object_url(key):
        break_string = '?AWSAccessKeyId'
        pre_assigned_url = s3.generate_presigned_url('get_object', 
        Params={'Bucket': self.bucket_name, 'Key': key})
        pre_assigned_url = pre_assigned_url.split(break_string)[0]
        return pre_assigned_url



def get_object_url(bucket,key):
    break_string = '?AWSAccessKeyId'
    pre_assigned_url = s3.generate_presigned_url('get_object', 
    Params={'Bucket': bucket, 'Key': key})
    pre_assigned_url = pre_assigned_url.split(break_string)[0]
    return pre_assigned_url


def send_sqs_message(queue_name,message):
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    response = queue.send_message(MessageBody=message)


