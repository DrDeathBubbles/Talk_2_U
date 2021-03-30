import vimeo
import os 
import time 
import sys
import os

client = vimeo.VimeoClient(
    token = os.environ['VIMEO_ACCESS_TOKEN'],
    key = os.environ['VIMEO_CLIENT_ID'],
    secret = os.environ['VIMEO_CLIENT_SECRET']
)



def vimeo_upload(file_name, title, description,privacy='anybody'):
    file_name = os.path.abspath(file_name)
    
    uri = client.upload(file_name, data={
        'name':f'{title}',
        'description':f'{description}',
        'privacy':{'view':f'{privacy}'}
    })

    while True: 
        response = client.get(uri + '?fields=transcode.status').json()
        if response['transcode']['status'] == 'complete':
          print('Your video finished transcoding.')
          break
        elif response['transcode']['status'] == 'in_progress':
          print('Your video is still transcoding.')
        else:
          print('Your video encountered an error during transcoding.')
          return -1 
        time.sleep(60)  


    response = client.get(uri + '?fields=link').json()
    return response['link']
