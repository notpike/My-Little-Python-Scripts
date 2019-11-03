#!/usr/bin/python3

import tweepy
import random

#Creds
#https://apps.twitter.com
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

#Auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Tweet ID
tweet = 999898775379365888

def winnerWinnerChickenDinner(tweet):
    results = api.retweeters(tweet)
    nResults = []
    for ID in results:
        nResults.append(api.get_user(ID).screen_name)

    #Winning
    sysRandom = random.SystemRandom()    
    print(sysRandom.choice(nResults))
    print(sysRandom.choice(nResults))
    print(sysRandom.choice(nResults))

if __name__ == "__main__":
    winnerWinnerChickenDinner(tweet)
