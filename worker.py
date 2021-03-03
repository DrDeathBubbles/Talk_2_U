import logging
import multiprocessing 
from time import sleep
from random import random, randint
from video_processing import video_processing
from aws import s3_bucket


logger = logging.getLogger(__name__)  # use module name


def cleanup_files(raw_file, ed_file):
    os.remove(raw_file)
    os.remove(ed_file)



def video_processing(listner_queue, task_queue, redis_database, input_bucket = 'cc21-raw',
output_bucket = 'cc21-ed', raw_location = '~/video_files/raw/', 
ed_location = '~/video_files/ed/', sting = '~/video_files/assets/sting.mp4',
watermark = '~/video_files/assets/watermark.png'):
    process_name = multiprocessing.current_process().name
    input_bucket = s3_bucket(input_bucket)
    output_bucket = s3_bucket(output_bucket)
    talkot_vimeo = 

    while True:
        edited_url = 'Not generated'
        tasks = task_queue.get()
        key = tasks[0]
        raw_file = raw_location + key
        ed_file = ed_location + key
        
        
        if key == 0:
            print(f"{process_name} process quits")
        else:
            print(f"{process_name} recieved {key}".format(process_name,key))
            try:
                input_bucket.retrieve_from_s3(key,raw_file)
                print('{} retrieves from S3'.format(process_name))
            except Exception as e:
               logger.log(logging.ERROR,'Problem retrieving {}'.format(key))
               print(f'Problem retrieving {key}')
               continue

            try: 
                video_processing(process_name, raw_file, sting, watermark, ed_file)

            except:
                logger.critical(f"{key} failed to video process.")

            try:
                edited_url = output_bucket.post_to_s3(ed_file)

            except:                                       
                logger.error(f"{key} failed to produce video url.")

            try:
                redis_database.update_field(key,'s3_processed', edited_url)

            except:                    
                logger.error(f"{key} failed to update redis.")
         
            try:
                cleanup_files(raw_file,ed_file)    

            except:
               logger.error(f"{key} failed to cleanup")


            try:

            except:



            #Send SQS to vimeo upload    
            





def worker_process(listner_queue,task_queue):
    for i in range(3):
        sleep(random())
        logger.info(f'Logging a random number {randint(0, 10)}')