import boto3

from aws import get_object_url, send_sqs_message

try:
    from urllib.parse import unquote 
except ImportError:
     from urlparse import unquote



def __main__(region,input_queue):
    sqs = boto3.resource('sqs',region_name = region)
    q = sqs.get_queue_by_name(QueueName= input_queue)
    r = redis.Redis(host='localhost', port = 6379, db=0,decode_responses=True)

    redis_fields = {'primary_key':'unset',
    's3_raw':'unset',
    's3_processed':'unset',
    'transcript':'unset',
    'vimeo':'unset',
    'audio':'unset',
    }

    while True:
        keys = []
        rs = q.receive_messages()
        for m in rs:
            temp = json.loads(m.body)
            m.delete()
            try:
                key = temp['Records'][0]['s3']['object']['key']
                key = unquote(temp)
            except KeyError as ke:
                logging.error('A key error {} has occured while trying\
                to access the S3 filename.')
            keys.append(key)

        for k in keys:
            upload_fields = redis_fields.copy()
            object_url = get_object_url(k)
            upload_fields['primary_key'] = k
            upload_fields['s3_raw'] = object_url


            
