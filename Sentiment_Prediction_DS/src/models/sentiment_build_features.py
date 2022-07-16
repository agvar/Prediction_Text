import pandas as pd
import numpy as np
import sklearn
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import ngrams
from sklearn.model_selection import train_test_split
from datetime import datetime
from pathlib import Path
import re
import warnings
warnings.filterwarnings('ignore')
 

def text_cleanse(text):
    """
    remove @,non alphanumeric character like or punctuations,url links,numerals,stopwords
    
    """
    
    text=re.sub(r'[^\w\s]','',text)        
    text=re.sub(r'https?\S+','',text)       
    text=re.sub(r'@\S+|#\S+','',text)        
    text=re.sub(r'[0-9]+','',text) 
    return text

def text_remove_stopwords(text):
    '''
    The words 'no' and 'not' are removed from the default stopwords list. 
    The text is split into words and stopwords removed
    '''
    stopwords_updated=[word for word in stopwords.words('english') if word not  in ['no','not'] ]
    text=" ".join([word.lower() for word in text.split() if word not in stopwords_updated])
    return text

def text_tokenize(text):
     return word_tokenize(text)

def text_stemming(text):
    return [SnowballStemmer('english').stem(word) for word in text]

def text_lemmatize(text):
    return ' '.join(WordNetLemmatizer().lemmatize(word) for word in text)



