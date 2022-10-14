# Overview

The project predicts the sentiment ( positive or negetive ) on real-time tweets . Tweets are read using the tweepy API and pushed into a Kinesis data stream . A consumer python proces reads these tweets and calls the prediction API to predict the sentiment.
The API is a Django application that uses a Linear Regression model to make predictions. The response predications are displayed on a dashboard to depict trends.
The twitter topic to be used when pulling tweets can be configured ,along with the number of tweets to be pulled.
The raw tweets and the predictions are stored on AWS S3 as json files

## Data and Process Flow

![Architecture Diagram](https://github.com/agvar/Prediction_Text/blob/master/images/capstone_project_architecture.jpeg)

## Data Analysis

The analysis done on the datasets is at : https://github.com/agvar/Prediction_Text/blob/2acd88106dab4106de90d4dc10e5608af0af78c7/Sentiment_Prediction_DS/notebooks/Sentiment_analysis.ipynb

## Project Organization

    ├── LICENSE
    ├── README.md                  <- The top-level README for developers using this project.
    ├── Prediction_API             <- Django API folder
    ├── Sentiment_Prediction_DS    <- Python notebooks ,models folder
    ├── twitter_streaming          <- consumer and producer modules for reading from tweepy and writing to Kineses, S3
    └── images                     <- images,diagrams for the project
