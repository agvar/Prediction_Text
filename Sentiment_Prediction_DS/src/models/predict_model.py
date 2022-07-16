from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
import logging
from features.sentiment_build_features import text_cleanse,text_remove_stopwords,text_tokenize,text_stemming,text_lemmatize
from sentiment_model import Model
import joblib


model_path= Path(__file__).resolve().parents[2] / "models" / "model.joblib"
vectorizer_path= Path(__file__).resolve().parents[2] / "models" / "vectorizer.joblib"

print('loading model')
with open(model_path,'rb') as f:
    loaded_model=joblib.load(f)

print('loading vectorizer')
with open(vectorizer_path,'rb') as f:
    loaded_vectorizer=joblib.load(f)

print('Enter text')
input_text='not  Horrible instance'
cleaned_text=text_cleanse(input_text)
stopwords_removed_text=text_remove_stopwords(cleaned_text)
tokenized_text=text_tokenize(stopwords_removed_text)
stemmed_text=text_stemming(tokenized_text)
lemmatized_text=text_lemmatize(stemmed_text)
print(lemmatized_text)


X=loaded_vectorizer.transform([lemmatized_text])
prediction=loaded_model.predict(X)
print(prediction)
