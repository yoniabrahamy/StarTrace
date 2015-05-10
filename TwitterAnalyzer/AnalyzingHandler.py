import collections
import argparse
import json
import datetime
import random
import os
import pickle
from datetime import timedelta
from TwitterQuerier import TwitterQuerier

class AnalyzingHandler:
    #start __init__
    #def __init__(self):  // Remove if ctor is necessary
    #end

    def analyzeTweets(self, keyword, location=None, until=None):
      #Getting some tweets
      querier = TwitterQuerier()
      tweets = querier.getTweets(keyword, location=location)

      # TODO: Call learning machine

      # TODO: Create a streamer that gets tweets and saves the to the database

      # IMPORTANT: THIS IS A PLACEHOLDER! REPLACE WITH ACTUAL RESULTS!
      results = {'positive':33, 'negative':33, 'neutral':33}

      return results;

    #end LearnTweets

#end class

# Test Entry point
#analyzer = AnalyzingHandler()

#print analyzer.analyzeTweets('love', location='United States')