import botocore.session
session = botocore.session.get_session()
s3 = session.create_client('s3')
s3._client_config.signature_version = botocore.UNSIGNED

sqs = boto3.resource('sqs')

def get_object_url(bucket,key):
    break_string = '?AWSAccessKeyId'
    pre_assigned_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key})
    pre_assigned_url = pre_assigned_url.split(break_string)[0]
    return pre_assigned_url


def send_sqs_message(queue_name,message):
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    response = queue.send_message(MessageBody=message)


