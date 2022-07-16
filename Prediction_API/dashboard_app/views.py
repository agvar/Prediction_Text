from django.shortcuts import render
import pandas as pd
import boto3
import datetime.datetime 


s3_bucket = 'dataset20200101projectfiles'
s3_resource = boto3.resource('s3')
s3_stream_folder = 'capstone/output_tweets/streaming/'
for file in s3_resource.Bucket(s3_bucket).objects.filter(Prefix=s3_stream_folder):
    if file.last_modified.replace(tzinfo = None) > datetime.datetime(YEAR,MONTH, DAY,tzinfo = None):


sentiment_colls=['sentiment','tweet_id','tweet_date','query','username','tweet']
tweet_df=pd.read_csv(input_file_sentiment,encoding='cp1252',names=sentiment_colls,usecols=['sentiment','tweet'])
#if s3_status==200:
    #sentiment_colls=['sentiment','tweet_id','tweet_date','query','username','tweet']
    #tweet_df=pd.read_csv(s3_file.get("Body"),compression='zip',encoding='cp1252',names=sentiment_colls,usecols=['sentiment','tweet'])

#else:
    #print(f"s3 file not read")
print("complete input file")


def dashboard(request):
    return render(request,"dashboard_app/base.html")

# Create your views here.
