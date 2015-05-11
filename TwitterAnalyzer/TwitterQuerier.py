import collections
import argparse
import urllib
import urllib2
import json
import datetime
import random
import os
import pickle
from datetime import timedelta
from geopy.geocoders import GeoNames
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager

class TwitterQuerier:
    #start __init__
    #def __init__(self):  // Remove if ctor is necessary
    #end
    #start getTweets
    def getTweets(self, keyword, location=None , until=None):
        params = {}

        # Checking for params
        if (until != None):
            params['until'] = until
        if (location != None):
            geopoint = self.extractLocation(location)

            # If no longtitude and latitude found, not including locations in search
            if (geopoint != None):
                params['geocode'] = "%f,%f,2000km" % (geopoint['latitude'], geopoint['longitude'])
        return self.getData(keyword, params)
    #end
    #start extractLocation
    def extractLocation(self, location):

        geolocator = GeoNames(username='startrace')
        geolocation = geolocator.geocode(location, timeout=10000)

        geopoint = {}

        if geolocation == None:
            return None;
        else:
            geopoint['latitude'] = geolocation.latitude
            geopoint['longitude'] = geolocation.longitude
            return geopoint
    #end
    def parse_config(self):
      config = {}
      # from file args
      if os.path.exists('config.json'):
          with open('config.json') as f:
              config.update(json.load(f))
      else:
          # may be from command line
          parser = argparse.ArgumentParser()

          parser.add_argument('-ck', '--consumer_key', default=None, help='Your developper `Consumer Key`')
          parser.add_argument('-cs', '--consumer_secret', default=None, help='Your developper `Consumer Secret`')
          parser.add_argument('-at', '--access_token', default=None, help='A client `Access Token`')
          parser.add_argument('-ats', '--access_token_secret', default=None, help='A client `Access Token Secret`')

          args_ = parser.parse_args()
          def val(key):
            return config.get(key)\
                   or getattr(args_, key)\
                   or raw_input('Your developper `%s`: ' % key)
          config.update({
            'consumer_key': val('consumer_key'),
            'consumer_secret': val('consumer_secret'),
            'access_token': val('access_token'),
            'access_token_secret': val('access_token_secret'),
          })
      # should have something now
      return config

    def oauth_req(self, url, http_method="GET", post_body=None,
                  http_headers=None):
      config = self.parse_config()
      consumer = oauth2.Consumer(key=config.get('consumer_key'), secret=config.get('consumer_secret'))
      token = oauth2.Token(key=config.get('access_token'), secret=config.get('access_token_secret'))
      client = oauth2.Client(consumer, token)

      resp, content = client.request(
          url,
          method=http_method,
          body=post_body or '',
          headers=http_headers
      )
      return content

    def getTweeterApi(self):
        config = self.parse_config();
        api = TwitterAPI(config['consumer_key'], #consumer_key
                         config['consumer_secret'], #consumer_secret
                         config['access_token'], #access_token
                         config['access_token_secret']) #access_token_secret
        return api
    #end

    def getData(self, keyword, params):
        tweeter_api = self.getTweeterApi()

        #get the params
        data = {'q': keyword, 'lang': 'en', 'count' : 150}

        #Add if additional params are passed
        if params:
            for key, value in params.iteritems():
                data[key] = value

        results = tweeter_api.request('search/tweets', data)

        tweets = []
        for item in results:
            tweets.append(item['text']) # if 'text' in item else item)

        return tweets
    #end


#end class