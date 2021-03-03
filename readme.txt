
# SQS queues
* talkbot_s3
* talkbot_processing_priority
* talkbot_processing_normal
* talkbot_vimeo
* talkbot_transcription




# Redis setup

1) Allow redis keyspace events:
```bash
redis-cli config set notify-keyspace-events KEA
```
2)Start redis