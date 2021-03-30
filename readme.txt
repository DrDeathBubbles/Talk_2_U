
# SQS queues
* talkbot_s3
* talkbot_processing_priority
* talkbot_processing_normal
* talkbot_vimeo
* talkbot_transcription

    redis_schema = {'primary_key':'key',
    's3_raw':'unset',
    's3_processed':'unset',
    'transcript':'unset',
    'vimeo':'unset',
    'audio':'unset',
    'priority':0
    }


# Redis setup

1) Allow redis keyspace events:
```bash
redis-cli config set notify-keyspace-events KEA
```
2)Start redis


1. Open tunnel between processing system and scheduling system

        autossh -i ~/.ssh/steven_tobin.pem -N -f -L localhost:6378:localhost:6379 

        autossh -i ~/.ssh/steven_tobin.pem -N -f -L localhost:6378:localhost:6379 ubuntu@ec2-18-203-222-202.eu-west-1.compute.amazonaws.co
        i

To talkbot_video_processing        
autossh -i ~/.ssh/steven_tobin.pem -N -f -L localhost:6378:localhost:6379 ubuntu@ec2-63-32-61-101.eu-west-1.compute.amazonaws.com        

To talkbot_data
autossh -i ~/.ssh/steven_tobin.pem -N -f -L localhost:6378:localhost:6379 ubuntu@ec2-34-243-102-171.eu-west-1.compute.amazonaws.com   

