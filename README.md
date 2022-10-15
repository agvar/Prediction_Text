![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

# Twitter Sentiment Prediction

## Description

The project was created as part of the Machine Learning Bootcamp capstone project
The project predicts the sentiment ( positive or negetive ) on real-time tweets . Tweets are read using the tweepy API with a python Producer process, and pushed into a Kinesis data stream . A consumer python process reads the tweets and calls the prediction API to predict the sentiment.
The API is a Django application that uses a Logistic Regression model to make predictions. The response predications are displayed on a dashboard to depict trends.
The twitter topic to be used when pulling tweets can be configured ,along with the number of tweets to be pulled, at a time.
The raw tweets and the predictions are stored on AWS S3 as json files

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)

## Installation

To install the django api ->
To install the twitter consumer and producer ->
To install the ML prediction analysis,notebook ,data preprocessing ->

## Usage

## Process Flow

![Architecture Diagram](https://github.com/agvar/Prediction_Text/blob/master/images/capstone_project_architecture.jpeg)

## Data Analysis

The analysis done on the twitter train datasets is at : https://github.com/agvar/Prediction_Text/blob/2acd88106dab4106de90d4dc10e5608af0af78c7/Sentiment_Prediction_DS/notebooks/Sentiment_analysis.ipynb

## Project Organization

    ├── LICENSE
    ├── README.md                  <- The top-level README for developers using this project.
    ├── Prediction_API             <- Django API folder
    ├── Sentiment_Prediction_DS    <- Python notebooks ,models folder
    ├── twitter_streaming          <- consumer and producer modules for reading from tweepy and writing to Kineses, S3
    └── images                     <- images,diagrams for the project

## Credits

## License
