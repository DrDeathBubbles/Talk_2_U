import botocore.session
session = botocore.session.get_session()
s3 = session.create_client('s3')
s3._client_config.signature_version = botocore.UNSIGNED
bucket = 'ws20-output'
key ='AJM SQL TEST.txt'

def get_object_url(bucket,key):
    break_string = '?AWSAccessKeyId'
    pre_assigned_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key})
    pre_assigned_url = pre_assigned_url.split(break_string)[0]
    return pre_assigned_url

