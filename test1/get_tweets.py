from tweepy import OAuthHandler
import tweepy

import codecs
import time
import os
import re

res = re.compile(r'http://[a-zA-Z0-9.?/&=:]*|https://[a-zA-Z0-9.?/&=:]*', re.S)

consumer_key = "AopfNa0A9edEPEvCoGnvyg"
consumer_secret = "jKk5Wy6LILNWpalJNIzzdTc345CceoQL9fthEjD9Q"

access_token = "190671283-6E4IRCesrlc5yqGr8Ha56wbRH0S36nDCsmk0cdOs"
access_token_secret = "wzee8XXKlUMhKoIkx91lkp6O3yAFyGeFDewHOgRbalg"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def getTweets(query):
    #time.sleep(5)
    results = []
    inx = 0
    for tweet in tweepy.Cursor(api.search, q='%s' % query, lang='en').items():
        #results.append(tweet.text)
        #if len(results) > 100:
        if inx >= 100:
            break
        ss = tweet.text
        ss = res.sub("", ss)
        text = ' '.join(l.lower() for l in ss.strip().split())
        #text = ' '.join(l.low() for l in tweet.text.strip().split())
        yield text, inx
        inx += 1
    #print(query)
    print('length of tweets: %d' %(inx))

