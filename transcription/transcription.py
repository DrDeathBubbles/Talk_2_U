import boto3




class transcribe():

    def __init__(self):
        super().__init__()


    def aws_transcribe(self, job_name,job_uri):
        transcribe = boto3.client('transcribe', region_name = 'eu-west-1')
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='mp3',
            LanguageCode='en-US'
        )
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("Not ready yet...")
            time.sleep(5)
        return status


    def get_text(self,response):
        trans_url = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        text = requests.get(trans_url)
        text = text.json()
        text = text['results']['transcripts']
        text = text[0]['transcript']
        return text

    def run_trascription_job(job_name, job_uri):
        response = self.aws_transcribe(job_name, job_uri)
        text = self.get_text(response)
        return text    
