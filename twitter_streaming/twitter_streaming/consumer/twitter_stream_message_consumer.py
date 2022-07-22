import sys
import os
import tweepy
from datetime import datetime
import json
import argparse
import boto3
import requests
import configparser
from pathlib import Path
from dotenv import load_dotenv

def save_tweet_s3(s3_resource,data_list,s3_bucket,s3_folder):
    current_ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
    s3_file = s3_resource.Object(s3_bucket, s3_folder + current_ts + '.json')
    return_s3 = s3_file.put(Body=(bytes(json.dumps(data_list).encode('UTF-8'))))
    if return_s3['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(f"Failed to upload files to s3 bucket :{s3_bucket}")
        sys.exit(1)

def read_tweet_stream(s3_resource,kinesis_client,stream_name,sentiment_prediction_endpoint,comprehend,comprehend_language_cd):
    sentiment_score_map={'POSITIVE':4,
                     'NEGATIVE':0,
                     'NEUTRAL':2,
                     'MIXED':2
                     }
    try:
        response_shards = kinesis_client.list_shards(StreamName=stream_name)
    except Exception as e:
        print(f"Failed to get shards:{e}")

    for shard in response_shards['Shards']:
        try:
            response_shard_iterator=kinesis_client.get_shard_iterator(
                StreamName=stream_name,
                ShardId=shard['ShardId'],
                ShardIteratorType='TRIM_HORIZON'
                )
        except Exception as e:
            print(f"Failed to get shards:{e}")
        ShardId = shard['ShardId']
        ShardIterator=response_shard_iterator['ShardIterator']
        #print(f'shard id, shard iterator :{ShardId},{ShardIterator}')
        while ShardIterator:
            data_records=kinesis_client.get_records(ShardIterator=ShardIterator)
            if len(data_records['Records'])>0:
                tweet_list=[]
                for record in data_records['Records']:
                    tweets=json.loads(record['Data'])
                    for tweet in tweets:
                        if tweet['extended_tweet_text']:
                            tweet_text=tweet['extended_tweet_text']
                        else:
                            tweet_text = tweet['text']
                        tweet_json={'text' : tweet_text}
                        try:
                            sentiment_response_comprehend=comprehend.detect_sentiment(Text=tweet_text, LanguageCode=comprehend_language_cd)
                        except Exception as e:
                            print(f'unable to run detect sentiment on comprehend : {e}')
                            sys.exit(1)
                        try:
                            sentiment_response_model_api=requests.post(sentiment_prediction_endpoint,json=tweet_json)
                        except Exception as e:
                            print(f'unable to post request on {sentiment_prediction_endpoint}  : {e}') 
                            sys.exit(1)

                        tweet['comprehend_sentiment']=sentiment_response_comprehend.get('Sentiment')
                        tweet['comprehend_sentiment_score_overall'] = sentiment_score_map[sentiment_response_comprehend.get('Sentiment')]
                        tweet['comprehend_sentiment_score_positive'] = (sentiment_response_comprehend.get('SentimentScore')).get('Positive')
                        tweet['comprehend_sentiment_score_negetive'] = (sentiment_response_comprehend.get('SentimentScore')).get('Negative')
                        tweet['comprehend_sentiment_score_mixed'] = (sentiment_response_comprehend.get('SentimentScore')).get('Mixed')
                        tweet['comprehend_sentiment_score_neutral'] = (sentiment_response_comprehend.get('SentimentScore')).get('Neutral')
                        tweet['model_api_sentiment'] = json.loads(sentiment_response_model_api.text).get('Sentiment')
                        tweet_list.append(tweet)
                        save_tweet_s3(s3_resource,tweet_list,s3_bucket,s3_folder)
 
                ShardIterator=data_records['NextShardIterator']
            else:
                break

def main(region,stream_name,sentiment_prediction_endpoint,s3_bucket,s3_folder,comprehend_language_cd):
    try:
        kinesis_client=boto3.client('kinesis',region_name=region)
    except Exception as e:
        print(f'unable to connect to kinesis client: {e}')
        sys.exit(1)
    try:
        s3_resource = boto3.resource('s3')
    except Exception as e:
        print(f'unable to connect to s3: {e}')
        sys.exit(1)
    try:
        comprehend=boto3.client('comprehend',region_name=region)
    except Exception as e:
        print(f'unable to connect to comprehend: {e}')
        sys.exit(1)
    read_tweet_stream(s3_resource,kinesis_client,stream_name,sentiment_prediction_endpoint,comprehend,comprehend_language_cd)

if __name__=='__main__':
    try:
        dotenv_path=Path(__file__).resolve().parents[2]
        load_dotenv()
        API_key=os.getenv('API_key')
        API_secret_key=os.getenv('API_secret_key')
        Access_token=os.getenv('Access_token')
        Acess_token_secret=os.getenv('Acess_token_secret')
    except Exception as e:
        print(f"error reading from .env file at {dotenv_path}: {e}")
        sys.exit(1)
    
    try:
        config_path=Path(__file__).resolve().parents[2] / 'twitter_streaming.ini'
        config=configparser.ConfigParser()
        config.read(config_path)
        region=config.get('AWS resources','region')
        stream_name=config.get('AWS resources','stream_name')
        sentiment_prediction_endpoint=config.get('AWS resources','sentiment_prediction_endpoint')
        comprehend_language_cd=config.get('AWS resources','comprehend_language_cd')
        s3_bucket=config.get('AWS resources','s3_bucket')
        s3_folder=config.get('AWS resources','s3_folder_output')
    except Exception as e:
        print(f"error reading from {config_path}:{e}")
        sys.exit(1)
    
    main(region,stream_name,sentiment_prediction_endpoint,s3_bucket,s3_folder,comprehend_language_cd)
    





