import pandas as pd
import numpy as np
import sklearn
import nltk
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score,roc_curve,auc
from datetime import datetime
from pathlib import Path
import re
import warnings
warnings.filterwarnings('ignore')
import logging
from sentiment_build_features import text_cleanse,text_remove_stopwords,text_tokenize,text_stemming,text_lemmatize
from sentiment_model import Model
from sklearn.linear_model import LogisticRegression
import boto3
model_path= Path(__file__).resolve().parents[2] / "models" / "model.joblib"
vectorizer_path= Path(__file__).resolve().parents[2] / "models" / "vectorizer.joblib"



#s3_bucket = 'dataset20200101projectfiles'
#s3 = boto3.client('s3')
#s3_file = s3.get_object(Bucket=s3_bucket,Key='capstone/input_data/twitter_sentiment140/twitter_sentiment.zip')
#s3_status = s3_file.get("ResponseMetadata", {}).get("HTTPStatusCode")
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

print("clean input file")
   
df_cleaned=tweet_df[['tweet','sentiment']]
df_cleaned['tweet_cleaned']=df_cleaned['tweet'].apply(text_cleanse)
df_cleaned['tweet_remove_stopwords']=df_cleaned['tweet_cleaned'].apply(text_remove_stopwords)
df_cleaned['tweet_tokenized']=df_cleaned['tweet_cleaned'].apply(text_tokenize)
df_cleaned['tweet_stem']=df_cleaned['tweet_tokenized'].apply(text_stemming)
df_cleaned['tweet_lemma']=df_cleaned['tweet_stem'].apply(text_lemmatize)
print("clean input file complete")

X=df_cleaned['tweet_lemma']
y=df_cleaned['sentiment'].apply(lambda x:1 if x==4 else x)
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=40)

print('start vectorize')
model=Model()
vectorizer=model._vectorizer

vectorizer=vectorizer.fit(X_train)
X_train=vectorizer.transform(X_train)
X_test=vectorizer.transform(X_test)

print('end vectorize')
print('start training')
model.train(X_train,y_train)
print('end training')
print('save model')
model.save(model_path,vectorizer,vectorizer_path)
print('save model done')
y_pred=model.predict(X_test)
model.evaluate(y_test,y_pred)






