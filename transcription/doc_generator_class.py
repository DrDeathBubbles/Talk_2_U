from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import boto3
import json

from apiclient import discovery
import io
import oauth2client
from oauth2client import client
from oauth2client import tools
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


def service_generation():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    return [drive_service, service]


def doc_generator():

    def __init__:
        self.service_objects = service_generation()


    def doc_generation(vimeo_url='unset', s3_url = 'unset', uid = 'unset', 
    speakers = 'unset', text = 'unset', title ='unset',
    drive_service = self.service[0],service = self.service_objects[1]):

        document_id = '1szDKqGQYj0w8eze0D5YHr5kJ-XyooagV-moK6-kmK08'
        copy_title = title 
        body = {
            'name': copy_title,
            'parents': ['123a9rNtXvbQeo1etgTXmTAe6G4-XLDPp']
        }
        drive_response = drive_service.files().copy(
        fileId=document_id, body=body).execute()
        document_copy_id = drive_response.get('id')



        requests = [
             {
                'replaceAllText': {
                    'containsText': {
                        'text': '{{title}}',
                        'matchCase':  'true'
                    },
                    'replaceText': title,
                }},

                {
                'replaceAllText': {
                    'containsText': {
                        'text': '{{speakers}}',
                        'matchCase':  'true'
                    },
                    'replaceText': speakers,
                }}, 

                 {
                'replaceAllText': {
                    'containsText': {
                        'text': '{{vimeo_url}}',
                        'matchCase':  'true'
                    },
                    'replaceText': vimeo_url,
                }}, 

                 {
                'replaceAllText': {
                    'containsText': {
                        'text': '{{s3_url}}',
                        'matchCase':  'true'
                    },
                    'replaceText': s3_url,
                }}, 

                 {
                'replaceAllText': {
                    'containsText': {
                        'text': '{{text}}',
                        'matchCase':  'true'
                    },
                    'replaceText': text,
                }
            }
        ]

        result = service.documents().batchUpdate(
            documentId=document_copy_id, body={'requests': requests}).execute()

        return result        








if __name__ == '__main__':


    #get key for text and data - check if exists in external, if not, generate with blank, if there, imput data
    # If put data in, send message to update 


    ser =service_generation()

    sqs = boto3.resource('sqs',region_name = 'eu-west-1')
    q = sqs.get_queue_by_name(QueueName='Babble')    

    while True:
        messages = []
        rs = q.receive_messages()
        for m in rs:
            temp = json.loads(m.body)
            temp = json_processing(temp)
             #To be put back in after testing
            try:
                doc_generation(ser[0], ser[1],**temp)
                m.delete()
                print('Doc generated!')

            except:
                print('Failed to make doc of transcript')
                pass    
















