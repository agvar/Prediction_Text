from django.shortcuts import render
import pandas as pd
import boto3

s3_bucket = 'dataset20200101projectfiles'
s3 = boto3.client('s3')
s3_file = s3.get_object(Bucket=s3_bucket,Key='capstone/input_data/twitter_sentiment140/twitter_sentiment.zip')
s3_status = s3_file.get("ResponseMetadata", {}).get("HTTPStatusCode")
print("read input file")
input_file_sentiment="E:\\python_projects\\Springboard\datasets\\twitter_sentiment140\\training_140_sentiment.csv"
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
