import pandas as pd
import numpy as np
import sklearn
import nltk
import pickle
import joblib
import seaborn as sns
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score,roc_curve,auc
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot as plt
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
from sklearn.feature_extraction.text import TfidfVectorizer

class Model:
    def __init__(self):
        self._model=LogisticRegression()
        self._vectorizer=TfidfVectorizer(max_features=500000)
        
    def train(self,X,y):
        return self._model.fit(X,y)     
    
    def predict(self,X):
        return self._model.predict(X)
    
    def save(self,model_path,vectorizer,vectorizer_path):
        self._vectorizer=vectorizer
        if self._vectorizer and vectorizer_path:
            joblib.dump(self._vectorizer,vectorizer_path)
        else:
            raise TypeError("vectorizer or path not specified" )

        if self._model and model_path:
            joblib.dump(self._model,model_path)
        else:
            raise TypeError("model not trained")
    
    def load(self):
        try:
            self._model=joblib.load(self._model_path)
        except:
            self._model_path=None
        return self

    def evaluate(self,y,y_pred):
        print(f'accuracy score: {accuracy_score(y,y_pred)}')
        print(classification_report(y,y_pred))
        conf_matrix=confusion_matrix(y,y_pred)
        print(f'confusion_matrix\n')
        print(f'True Negetives : {conf_matrix[0][0]}')
        print(f'False Negetive : {conf_matrix[0][1]}')
        print(f'False Positive : {conf_matrix[1][0]}')
        print(f'True Positive : {conf_matrix[1][1]}')
            
        fpr,tpr,thresholds=roc_curve(y,y_pred)
        auc_roc=auc(fpr,tpr)
        fig,ax=plt.subplots(1,2,figsize=(10,5))
        fig.tight_layout(pad=6)
        ax[0].plot(fpr,tpr,color='green',label='ROC Curve(area under curve : %0.00f)'% auc_roc)
        
        ax[0].set(title='ROC Curve',xlabel='False Positive Rate',ylabel='True Positive Rate')
        ax[0].grid(True)
        ax[1]=sns.heatmap(conf_matrix,cmap='Blues')
        ax[1].set(title='Confusion Matrix',ylabel='Actual Values',xlabel='Predicted Values')
        plt.show()
        

   