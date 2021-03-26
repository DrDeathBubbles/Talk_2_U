
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