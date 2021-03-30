import botocore.session
import boto3
#session = botocore.session.get_session()
#s3 = session.create_client('s3', region_name = 'eu-west-1')
#s3._client_config.signature_version = botocore.UNSIGNED

#sqs = boto3.resource('sqs', region_name = 'eu-west-1')



class s3_bucket():

    def __init__(self, bucket_name):
        self.session = botocore.session.get_session() 
        self.s3_client = self.session.create_client('s3', region_name = 'eu-west-1') 
        self.s3 = boto3.resource('s3')
        self.bucket_name = bucket_name
        self.bucket =  self.s3.Bucket(bucket_name) 


    def retrieve_from_s3(self, key, local_file):
        out = self.bucket.download_file(key, local_file)
        return out

    def post_to_s3(self, local_file, key):
        out = self.bucket.upload_file(local_file, key)
        url = self.get_object_url(key)
        return url

    def get_object_url(self, key):
        break_string = '?AWSAccessKeyId'
        pre_assigned_url = self.s3_client.generate_presigned_url('get_object', 
        Params={'Bucket': self.bucket_name, 'Key': key})
        pre_assigned_url = pre_assigned_url.split(break_string)[0]
        return pre_assigned_url

    def get_file_list_url(self):
        my_bucket = self.bucket
        get_last_modified = lambda obj: int(obj.last_modified.strftime('%s'))
        unsorted = []
        for f in my_bucket.objects.filter():
            unsorted.append(f)
        files = [obj.key for obj in sorted(unsorted, key=get_last_modified, reverse=True)][1:]
        files_url = [self.get_object_url(f) for f in files]
        #files_url = ['https://s3-eu-west-1.amazonaws.com/' + self.bucket_name + '/' + f for f in files]
        return list(zip(*[files,files_url])) 

    



