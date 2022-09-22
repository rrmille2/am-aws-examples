#!/usr/bin/env python3

import tweepy as tw
import json
import sys
import os

API_KEY = 'OAYQkmEUuGJJ4eCOaJqdtJZr6'
API_SECRET = 'mFWoW6vsbmMF7tJGjMz1Wg6NpJ1ZL39Q54NRdWvyzKbV1TgpFk'

# for AshMillFL
ACCESS_TOKEN = '1373974588095356936-baZAkU8IBbutYZg1ZNHgijciyHkiWL'
ACCESS_SECRET = 'tpa0E0b99RgblRjSBGNGNjJDQvApPliQwyNWX7tXXPU2g'

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAA%2BWSQEAAAAAwoRYphEXD5q64BmE3yZD4FJ3Jno%3DhgvZfn4nT0E5fyrhZaFC3Nyconky7luAUuovvntTPn0N0ZvaGo'

auth = tw.OAuthHandler(API_KEY, API_SECRET)
# the following line is only if we need to do user-specific operations (i.e., as AshMillFL)
#auth.set_access_token(ACCESS_TOKEN, SECRET_TOKEN)
api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# get command line arguments
if len(sys.argv) < 2:
    print('usage: {} <string1 string2 ...>'.format(sys.argv[0]))
    exit(-1)

search_words = []
for arg in sys.argv[1:]:
    search_words.append(arg)

# Define the search term and the date_since date as variables
date_since = "2019-01-01"

# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items()

# Iterate and print tweets
for tweet in tweets:
    tweet = tweet._json
    for item in tweet:
        print('{}: {}'.format(item, tweet[item])) 
    

