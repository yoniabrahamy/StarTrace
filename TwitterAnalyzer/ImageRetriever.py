import collections
import argparse
import json
import datetime
import os
from datetime import timedelta
import urllib
import urllib2
import socket

class ImageRetriever:
    #start __init__
    #def __init__(self):
    #end

    def retreiveImage(self, keyword):

      # Creating a dictionary for the url
      data = {'v': '1.0', 'q' : keyword, 'userip' : socket.gethostbyname(socket.gethostname())}

      queryString = urllib.urlencode(data);

      #Getting some images
      url = ('https://ajax.googleapis.com/ajax/services/search/images?' + queryString)

      request = urllib2.Request(url, None, {'Referer1': 'www.startrace.com'})
      response = urllib2.urlopen(request)

      # Process the JSON string.
      results = json.load(response)
      # now have some fun with the results...
      #

      PhotoUrls = [];
      rawPhotos = results['responseData']['results']

      for photo in rawPhotos:
        PhotoUrls.append(photo['unescapedUrl'])

      return PhotoUrls
    #end

#end class

# Test Entry point
#imager = ImageRetriever();
#print imager.retreiveImage('Brad Pitt')
#print results
#print results["responseData"]["results"][0]['unescapedUrl']