from tweepy import OAuthHandler, AppAuthHandler, API, Cursor
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import re
import os
import time
from datetime import datetime, date, timedelta

api_key = 'agQmGHFcg9CDeoUSXUFvdPl lT'
api_key_secret = 'N9rqHRmzCJt4SALlxWOCbYyXno0khHnbFTwBFVnrqEKWA1VlfL'
access_token = '141631266-H1XhbzZ7yslwVb8cjyyNUdIUzZT0A8YSHgFiphBa'
access_token_secret = 'vmqkCGJ6vgLW90Q9Sd4JM1p6WIDSbL1SjmK7Hs0Mhm5Ax'

auth = OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

list_of_dates = []
today = date.today()
for i in range(-7,1):
    target_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
    list_of_dates.append(target_date)


list_of_dicts = []
search_term = 'covid19 covid vaccine'
num_tweets = 16000

for end_date in list_of_dates:
    start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=1)).strftime("%Y-%m-%d") # Create 1-day windows for extraction
    tweet_count = len(list_of_dicts)

    for tweet in Cursor(api.search,
                                q=f'{search_term} since:{start_date} until:{end_date}',
                                lang = 'en',
                                count = num_tweets,
                                tweet_mode = 'extended').items(num_tweets):
        if (not tweet.retweeted) and ('RT @' not in tweet.full_text):
            if tweet.lang == "en":
                tweet_dict = {}
                tweet_dict['username'] = tweet.user.name
                tweet_dict['location'] = tweet.user.location
                tweet_dict['text'] = tweet.full_text
                #tweet_dict['fav_count'] = tweet.favorite_count  
                tweet_dict['hashtags'] = tweet.entities['hashtags']
                tweet_dict['tweet_date'] = tweet.created_at
                list_of_dicts.append(tweet_dict)
                tweet_count +=1
                print(f'Extracted tweet count = {tweet_count}')
            
    print(f'Completed extraction for {start_date} to {end_date}. Sleep for 15 mins')
    time.sleep(900)
    print('Ready to go again')