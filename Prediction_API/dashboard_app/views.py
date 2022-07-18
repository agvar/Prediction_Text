from django.shortcuts import render
import pandas as pd
import boto3
from datetime import datetime
from botocore.errorfactory import ClientError
import sys
from itertools import chain
import json

s3_bucket = 'dataset20200101projectfiles'
s3_stream_folder = 'capstone/output_tweets/streaming/'
file_loc_ts_s3='capstone/output_tweets/last_updated_ts/last_updated_ts.csv'
default_ts='1973-01-01 00:00:00'
columns=['tweet_id', 'created_at', 'text', 'extended_tweet_text', 'source',
'user', 'followers_count', 'friends_count', 'geo_enabled', 'time_zone',
'geo', 'coordinates', 'comprehend_sentiment',
'comprehend_sentiment_score_overall',
'comprehend_sentiment_score_positive',
'comprehend_sentiment_score_negetive',
'comprehend_sentiment_score_mixed',
'comprehend_sentiment_score_neutral', 'model_api_sentiment']

try:
    s3_resource = boto3.resource('s3')
except Exception as e:
    print(f'cannot connect to aws s3: {e}')
    sys.exit(1)

def get_latest_ts_s3() :
    try:
        s3_resource.Object(s3_bucket,file_loc_ts_s3).load()
        s3_file_ts=s3_resource.Object(s3_bucket,file_loc_ts_s3)
        ts_latest_s3=datetime.strptime(s3_file_ts.get()['Body'].read().decode('utf-8'),'%Y-%m-%d %H:%M:%S') 
    except ClientError: 
        print(f"s3 latest timestamp not found , using default date of {default_ts}")
        print(ClientError)
        ts_latest_s3=datetime.strptime(default_ts,'%Y-%m-%d %H:%M:%S') 
        return ts_latest_s3

def get_latest_filedata(ts_latest_s3):   
    ts_list=[]
    counter=0
    df_filelist=pd.DataFrame(columns=columns)
    for file in s3_resource.Bucket(s3_bucket).objects.filter(Prefix=s3_stream_folder):
        file_last_mod_ts=file.last_modified.replace(tzinfo = None)
        if file_last_mod_ts > ts_latest_s3:
            
            try:
                data=file.get()['Body'].read()#.decode('utf-8')
                if data:
                    json_data=json.loads(data)
                    df=pd.DataFrame(json_data)
                    df_filelist=pd.concat([df,df_filelist])
                    ts_list.append(file_last_mod_ts)
                    counter+=1
            except Exception as e:
                print(f"problem with json.loads {e}")
        if len(ts_list)>0:
            ts_list.sort()
            latest_ts_updated=ts_list[-1]
            latest_ts_updated_bytes=datetime.strftime(latest_ts_updated,'%Y-%m-%d %H:%M:%S').encode('utf-8')
        else:
            print(f"No file in s3 location : {s3_bucket}/{s3_stream_folder} after latest timestamp of {ts_latest_s3}")

def save_latest_ts_s3(s3_file_ts,latest_ts_updated_bytes):
    try:
            s3_file_ts.put(Body=latest_ts_updated_bytes)
            print(f"latest timestamp updated is {s3_file_ts.get()['Body'].read().decode('utf-8')}")
    except ClientError as e:
            print(f"Unable to save timestamp file -{e}")


def dashboard(request):
    return render(request,"dashboard_app/base.html")

# Create your views here.
