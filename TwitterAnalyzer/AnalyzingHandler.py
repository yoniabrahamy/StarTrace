import collections
import argparse
import json
import datetime
import random
import os
import pickle
from datetime import timedelta
from TwitterQuerier import TwitterQuerier
from TwitterLearningMachine import TwitterLearningMachine

class AnalyzingHandler:
    #start __init__
    def __init__(self):
      self.TwitterLM = TwitterLearningMachine('data/sampleTweets.csv')
    #end

    def analyzeTweets(self, keyword, location=None, until=None):
      #Getting some tweets
      querier = TwitterQuerier()
      tweets = querier.getTweets(keyword, location=location)

      # TODO: Call learning machine
      results = results = {'positive':0, 'negative':0, 'neutral':0}

      if len(tweets) > 0:
        for tweet in tweets:
          sentiment = self.TwitterLM.classify(tweet)
          results[sentiment] = results[sentiment] + 1

        # Normalizing the results:
        for key in results:
          results[key] = (results[key] * 100) / len(tweets)

      # TODO: Create a streamer that gets tweets and saves the to the database

      return results;

    #end LearnTweets

#end class

# Test Entry point
#analyzer = AnalyzingHandler()

#print analyzer.analyzeTweets('Beyonce', location='United States')