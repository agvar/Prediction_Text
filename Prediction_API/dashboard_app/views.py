from django.shortcuts import render
import pandas as pd
import boto3
from datetime import datetime
from botocore.errorfactory import ClientError
import sys
from itertools import chain, count
import json
from plotly.offline import plot
import plotly.express as px
import numpy as np
from pathlib import Path

s3_bucket = 'dataset20200101projectfiles'
s3_stream_folder = 'capstone/output_tweets/streaming/'
file_loc_ts_s3='capstone/output_tweets/last_updated_ts/last_updated_ts.csv'
default_ts='1973-01-01 00:00:00'

columns=['tweet_id', 'created_at', 'text', 'extended_tweet_text', 'source','user', 'followers_count', 'friends_count', 'geo_enabled', 'time_zone','geo', 'coordinates', 'comprehend_sentiment',
'comprehend_sentiment_score_overall','comprehend_sentiment_score_positive','comprehend_sentiment_score_negetive',
'comprehend_sentiment_score_mixed','comprehend_sentiment_score_neutral', 'model_api_sentiment']

try:
    s3_resource = boto3.resource('s3')
except Exception as e:
    print(f'cannot connect to aws s3: {e}')
    sys.exit(1)
try:
    s3_file_ts=s3_resource.Object(s3_bucket,file_loc_ts_s3)
except ClientError:
    print(e)
    sys.exit(1)


def get_latest_ts_s3(s3_bucket,file_loc_ts_s3) :
    try:
        s3_resource.Object(s3_bucket,file_loc_ts_s3).load()    
        ts_latest_s3=datetime.strptime(s3_file_ts.get()['Body'].read().decode('utf-8'),'%Y-%m-%d %H:%M:%S') 
    except ClientError: 
        print(f"s3 latest timestamp not found , using default date of {default_ts}")
        print(ClientError)
        ts_latest_s3=datetime.strptime(default_ts,'%Y-%m-%d %H:%M:%S') 
    return ts_latest_s3

def create_latest_dffiles(ts_latest_s3):   
    ts_list=[]
    counter=0
    print(f"latest timestamp : {ts_latest_s3}")
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
    
    if not df_filelist.empty:
        df_filelist['created_at_day']= pd.to_datetime(df_filelist.created_at).dt.date
        df_grp=df_filelist.groupby(['model_api_sentiment','created_at_day'])['tweet_id'].agg(['count']).reset_index()
        ts_list.sort()
        latest_ts_updated=ts_list[-1]   
        return df_grp,latest_ts_updated
    else:
        print(f"No file in s3 location : {s3_bucket}/{s3_stream_folder} after latest timestamp of {ts_latest_s3}")
        return None,None

def save_latest_ts_s3(s3_file_ts,latest_ts_updated):
    if s3_file_ts and latest_ts_updated:
        try:
                latest_ts_updated_bytes=datetime.strftime(latest_ts_updated,'%Y-%m-%d %H:%M:%S').encode('utf-8')
                s3_file_ts.put(Body=latest_ts_updated_bytes)
                print(f"latest timestamp updated is {s3_file_ts.get()['Body'].read().decode('utf-8')}")
        except ClientError as e:
                print(f"Unable to save timestamp file -{e}")
    else:
        print("no file to save")


def dashboard(request):
#if __name__=="__main__":
    start_time = datetime.now().time().strftime('%H:%M:%S')
    ts_latest_s3=get_latest_ts_s3(s3_bucket,file_loc_ts_s3)
    df_grp,latest_ts_updated=create_latest_dffiles(ts_latest_s3)
   
    end_time = datetime.now().time().strftime('%H:%M:%S')
    total_time=(datetime.strptime(end_time,'%H:%M:%S') - datetime.strptime(start_time,'%H:%M:%S'))
    print(f" time taken : {total_time}")
    #print(df_grp)
    fig=px.histogram(df_grp,x="created_at_day",y="count",color="model_api_sentiment")
    chart=fig.to_html()
    context={'chart':chart}
    #save_latest_ts_s3(s3_file_ts,latest_ts_updated)
    return render(request,'index.html',context)
    

# Create your views here.
