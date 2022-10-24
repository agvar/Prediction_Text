![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)

# Twitter Sentiment Prediction

## Description

The project was created as part of the Springboard Machine Learning Bootcamp capstone project.  
It predicts the sentiment ( positive or negetive ) on real-time tweets . Tweets are read using the tweepy API with a python Producer process, and pushed into a Kinesis data stream . A consumer python process reads the tweets and calls the prediction API to predict the sentiment.  
The API is a Django application that uses a Logistic Regression model to make predictions. The response predications are displayed on a dashboard to depict trends, in Django.  
The twitter topic to be used when pulling tweets can be configured ,along with the number of tweets to be pulled, at a time.
The raw tweets and the predictions are stored on AWS S3 as json files

## Table of Contents

- [Process Flow](#process-flow)
- [Data Collection](#data-collection)
- [Data preprocessing Model selection, training](#data-preprocessing,model-selection,-Model-training)
- [Installation](#installation)
- [Project Organization](#project-organization)
- [Credits](#credits)
- [License](#license)

## Data Collection

Datasets used:

Sentiment140 Dataset Details  
 **Source** : http://help.sentiment140.com/for-students  
 **Description**: The training data was automatically created, as opposed to having humans manual annotate tweets. In the approach used, any tweet with positive emoticons, like :), were positive, and tweets with negative emoticons, like :(, were negative. We used the Twitter Search API to collect these tweets by using keyword search. This is described in the following paper(https://cs.stanford.edu/people/alecmgo/papers/TwitterDistantSupervision09.pdf) The data is a CSV with emoticons removed.

## Data Pre-processing,Model selection, training

Data preprocessing ,vectorization ,evaluation of multiple models and training in the following notebook
[Notebook for model training ](https://github.com/agvar/Prediction_Text/blob/2acd88106dab4106de90d4dc10e5608af0af78c7/Sentiment_Prediction_DS/notebooks/Sentiment_analysis.ipynb)

## Installation

Clone the repository  
`git clone git@github.com:agvar/Deep_Learning_Text.git`

### Install django on AWS Elastic Beanstalk

To deploy the django project on elastic beanstalk:  
Follow the aws guide:  
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html  
The following changes need to be made after the initial Beanstalk deployment

1. The first time the env and application are created in EBS, make sure the only config file in the .ebextensions has the boiler plate code- make sure the application name is modified
   `option_settings:`
   `aws:elasticbeanstalk:container:python:`
   `WSGIPath: ebdjango.wsgi:application`
2. Check the eb status- the status would RED meaning the application is not ready or usable
3. change the config files to as follows
   **The django.config**
   `option_settings:`
   `aws:elasticbeanstalk:application:environment:`
   `DJANGO_SETTINGS_MODULE: "Prediction_API.settings"`
   `PYTHONPATH: "/var/app/current:$PYTHONPATH"`
   `aws:elasticbeanstalk:container:python:`
   `WSGIPath: Prediction_API.wsgi:application`

**The ngix.config**( This is added to increase the timeouts)  
`option_settings:`

- `namespace: aws:elb:policies`  
   `option_name: ConnectionSettingIdleTimeout`  
   `value: 300`  
  `files:`  
   `"/etc/nginx/conf.d/nginx.custom.conf":`  
   `mode: "644"`  
   `owner: "root"`  
   `group: "root"`  
   ` content: |`  
   `client_header_timeout 300;`  
   `client_body_timeout 300;`  
   ` send_timeout 300;`  
   `proxy_connect_timeout 300;`  
   `proxy_read_timeout 300;`  
   `proxy_send_timeout 300;`

`container_commands:`  
 `01_restart_nginx:`  
 `command: "sudo service nginx reload"`

4. change the settings.py django file as follows

`ALLOWED_HOSTS = ['<ebs service name>',' <IP address of the EC2 instance>']`

The first element is the ebs service, the other is the EC2 instance on the EBS

5. Deploy using eb deploy and run eb status again  
   (Always remember to add any changes to git before deploying)

#### Install the AWS Kinesis consumer and producer

`pip install -r requirements.txt`

Modify the ./twitter_streaming/twitter_streaming.ini file as needed to update the following:  
`stream_filter` ->set the filter on tweets to be processed  
`stream_language` -> sets the tweet language to look for  
`file_max_tweet_limit` -> maximum of tweets to be processed into a single json file  
`collect_max_tweet_limt` -> maximum of tweets to be processed on a single run.

**To execute Producer process**  
`python ./twitter_streaming/twitter_streaming/producer/twitter_stream_message_producer.py`

**To execute Consumer process**
`python ./twitter_streaming/twitter_streaming/consumer/twitter_stream_message_consumer.py`
The consumer process reads tweets from Kinesis and calls the tensorFlow api to make predictions and stores them on s3.

## Process Flow

![Architecture Diagram](https://github.com/agvar/Prediction_Text/blob/master/images/capstone_project_architecture.jpeg)

## Project Organization

    ├── LICENSE
    ├── README.md                  <- The top-level README for developers using this project.
    ├── Prediction_API             <- Django API folder
    ├── Sentiment_Prediction_DS    <- Python notebooks ,models folder
    ├── twitter_streaming          <- consumer and producer modules for reading from tweepy and writing to Kineses, S3
    └── images                     <- images,diagrams for the project

## Credits

https://ileriayo.github.io/markdown-badges/
https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html

## License

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
