import sys
import os
import tweepy
from datetime import datetime
import json
import argparse
import boto3
from twitter_credentials  import API_key,API_secret_key,Access_token,Acess_token_secret


def process_tweet(tweet):

    if "extended_tweet" in tweet:
        extended_tweet_text=tweet["extended_tweet"]["full_text"]
    else:
        extended_tweet_text=None
    if "text" in tweet:
        text = tweet["text"]
    else:
        text=None

    if "time_zone" in tweet["user"]:
        time_zone=tweet["user"]["time_zone"]
    else:
        time_zone=None

    data={"tweet_id":tweet["id"],
        "created_at":tweet["created_at"],
          "text":text,
          "extended_tweet_text":extended_tweet_text,
          "source":tweet["source"],
          "user":tweet["user"]["id"],
          "followers_count":tweet['user']["followers_count"],
          "friends_count":tweet['user']["friends_count"],
          "geo_enabled":tweet["user"]["geo_enabled"],
          "time_zone":time_zone,
          "geo":tweet["geo"],
          "coordinates":tweet["coordinates"]

        }
    return(data)

def save_tweet_s3(data_list):
    current_ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    s3_bucket = 'dataset20200101projectfiles'
    s3_file = s3.Object(s3_bucket, 'capstone/input_data/streaming/tweets_stream_' + current_ts + '.json')
    return_s3 = s3_file.put(Body=(bytes(json.dumps(data_list).encode('UTF-8'))))
    if return_s3['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Failed to upload files to s3 bucket :{s3_bucket}")
        sys.exit(1)

def push_tweet_stream(data_list):
    stream_name='tweet_stream'
    try:
        response_stream = kinesis_client.put_record(StreamName=stream_name, Data=json.dumps(data_list),PartitionKey='partition_key')

    except Exception as e:
        print(f"Failed writing to stream:{e}")

    if response_stream['ResponseMetadata']['HTTPStatusCode'] != 200:
        print("Failed to push data to stream :{stream_name}")
        sys.exit(1)
    shard_id=response_stream['ShardId']
    shard_sequence=response_stream['SequenceNumber']


#Streaming class override
class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self,file_max_tweet=100,collect_max_tweet=10):
        super(TwitterStreamListener,self).__init__()
        self.file_max_tweet=file_max_tweet
        self.tweet_counter=0
        self.data_list=[]
        self.collect_max_tweet=collect_max_tweet


    def on_status(self,status):
        tweet=status._json
        data=process_tweet(tweet)
        self.tweet_counter+=1
        if self.tweet_counter % 1000==0:
            print(f"Processed tweets:{self.tweet_counter}")
        if self.tweet_counter>self.collect_max_tweet:
            return False
        else:
            if len(self.data_list)<self.file_max_tweet:
                self.data_list.append(data)
                if len(self.data_list)==self.file_max_tweet:
                    save_tweet_s3(self.data_list)
                    push_tweet_stream(self.data_list)
                    self.data_list=[]

#       if status.retweeted:
#           return

    def on_error(self,status_code):
       print(f"Error status code is{status_code}")
       if status_code==420:
            return False

#main function
if __name__=='__main__':

    parser=argparse.ArgumentParser()
    parser.add_argument('file_max_tweet',help='The maximum number of tweeets to be stored in a file, needs to be less than 10,000,000',type=int)
    parser.add_argument('collect_max_tweet',help='The maximum number of tweeets to be collected, needs to be less than 100,000', type=int)
    args=parser.parse_args()

    if args.file_max_tweet>1000000 or args.collect_max_tweet>10000000:
        print("The maximum tweets to be collected or tweets per file are over the limit.")
        sys.exit(1)
    if args.file_max_tweet>args.collect_max_tweet:
        print("The maximum tweets to be collected cannot be greater than the tweets per file.")
        sys.exit(1)

    # Authentication and creation of an api object
    auth = tweepy.OAuthHandler(API_key, API_secret_key)
    auth.set_access_token(Access_token, Acess_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        print("Twitter Authentication OK")
    except Exception as e:
        print(f"Error during authentication{e}")

    #creating kinesis client and s3 resource
    try:
        kinesis_client=boto3.client('kinesis',region_name='us-west-2')
    except Exception as e:
        print(e)
        sys.exit(1)
    try:
        s3 = boto3.resource('s3')
    except Exception as e:
        print(e)
        sys.exit(1)

    #creating a stream to the twitter api
    twitterstreamlistener=TwitterStreamListener(args.file_max_tweet,args.collect_max_tweet)
    twitter_stream=tweepy.Stream(auth=api.auth,listener=twitterstreamlistener)
    twitter_stream.filter(track=["the","i","to","a","and","is","in","it","you","of","for","on","my","me","at","this"],languages=["en"])
    #twitter_stream.filter(track=None,languages=["en"])





