from tools.talkbot_s3 import s3_bucket
import os



def main():
    input_bucket = s3_bucket('cc21-raw')
    input_bucket.post_to_s3(os.path.abspath('./test/test_video.mp4'),'test_video.mp4')


if __name__ == '__main__':
    main()