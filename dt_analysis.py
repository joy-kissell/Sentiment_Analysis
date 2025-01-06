import tweepy
import pandas as pd
import re
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import download 

#nltk.download('vader_lexicon')

from dotenv import load_dotenv
import os

#loading in key to twitter
load_dotenv()

#authenticating my twitter development account
def authenticate_twitter():
    api_key = os.getenv("API_KEY")
    api_key_secret = os.getenv("API_SECRET")
    api_access = os.getenv("ACCESS_TOKEN")
    api_access_secret = os.getenv("ACCESS_SECRET")
    authenticate = tweepy.OAuthHandler(api_key,api_key_secret)
    authenticate.set_access_token(api_access,api_access_secret)
    return tweepy.API(authenticate, wait_on_rate_limit = True)

api = authenticate_twitter()

#to restrict time range of tweets
import datetime
#want to cover all options
query = "Donald Trump OR President Trump OR Trump"

#start term of presidency
range_1_start = "2017-01-20"
range_1_end = "2021-01-20"

#reelection
range_2_start = "2021-01-21"
range_2_end = "2024-11-05"

#fetching tweets that fit the query and each time range
def get_tweets(query, start, end):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", since=start, until=end).items(1000)
    return [tweet for tweet in tweets if not is_news_tweet(tweet)]

#trying to filter out news account tweets so it shows more public opinion
def is_news_tweet(tweet):
    news_keywords = ["news", "breaking", "breaking news", "update", "updates", "headline"]
    if any(keyword in tweet.text.lower() for keyword in news_keywords):
        return True
    #also factors out celebrities
    if tweet.user.verified:
        return True
    return False
first_term = get_tweets(query, range_1_start, range_1_end)
campaign_term = get_tweets(query, range_2_start, range_2_end)
#for later analysis
all_tweets = first_term + campaign_term
