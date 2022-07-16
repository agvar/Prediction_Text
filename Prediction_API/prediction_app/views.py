from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from pathlib import Path
import joblib
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
import logging
from .sentiment_build_features import text_cleanse,text_remove_stopwords,text_tokenize,text_stemming,text_lemmatize
from django.conf import settings
import nltk
nltk.download('stopwords', download_dir='/home/webapp/nltk_data')
nltk.download('punkt', download_dir='/home/webapp/nltk_data')
nltk.download('wordnet', download_dir='/home/webapp/nltk_data')
nltk.download('omw-1.4', download_dir='/home/webapp/nltk_data')

model_path=Path(settings.BASE_DIR) / 'prediction_app' / 'model.joblib'
vectorizer_path=Path(settings.BASE_DIR) / 'prediction_app' / 'vectorizer.joblib'

prediction_map={1: "Positive",0:"Negetive"}

with open(model_path,'rb') as f:
    loaded_model=joblib.load(f)

with open(vectorizer_path,'rb') as f:
    loaded_vectorizer=joblib.load(f)

def predict_sentiment(text):
    cleaned_text=text_cleanse(text)
    stopwords_removed_text=text_remove_stopwords(cleaned_text)
    tokenized_text=text_tokenize(stopwords_removed_text)
    stemmed_text=text_stemming(tokenized_text)
    lemmatized_text=text_lemmatize(stemmed_text)
    X=loaded_vectorizer.transform([lemmatized_text])
    prediction=loaded_model.predict(X)
    return prediction

# Create your views here.

@api_view(['GET'])
def home(request):
    return_value={
        "error_code" : "0",
        "info" : "success"
    }
    return Response(return_value)


@api_view(['POST'])
def predict(request):
    input_data=str(request.data.values())
    prediction=predict_sentiment(input_data)[0]
    predict_value=prediction_map.get(prediction,"Invalid sentiment")
    return_value={
        "error_code":"0",
        "Sentiment":predict_value
    }
    return Response(return_value)