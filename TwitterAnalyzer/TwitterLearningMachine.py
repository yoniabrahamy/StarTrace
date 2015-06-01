import collections
import datetime
from sklearn import svm
from sklearn import *
import nltk
from nltk.classify import *
import re
import csv
import pprint
import numpy
import classifier_helper
from classifier_helper import *
import pickle
import os.path

class TwitterLearningMachine:
    #start __init__
    def __init__(self, learningDataset):
      #define machines
      self.NBClassifier = None;
      self.SVMClassifier = None;

      #getting the stop words
      self.stopWords = self.getStopWordList('data/feature_list/stopwords.txt')
      self.featureList = []

      # init machines
      self.initNBClassifier(learningDataset)
    #end

    #start replaceTwoOrMore
    def replaceTwoOrMore(self, s):
        #look for 2 or more repetitions of character
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", s)
    #end

    #start process_tweet
    def processTweet(self, tweet):
        # process the tweets

        #Convert to lower case
        tweet = tweet.lower()
        #Convert www.* or https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','AT_USER',tweet)
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip('\'"')
        return tweet
    #end

    #start getStopWordList
    def getStopWordList(self, stopWordListFileName):
        #read the stopwords
        stopWords = []
        stopWords.append('AT_USER')
        stopWords.append('URL')

        fp = open(stopWordListFileName, 'r')
        line = fp.readline()
        while line:
            word = line.strip()
            stopWords.append(word)
            line = fp.readline()
        fp.close()
        return stopWords
    #end

    #start getfeatureVector
    def getFeatureVector(self, tweet, stopWords):
        featureVector = []
        words = tweet.split()
        for w in words:
            #replace two or more with two occurrences
            w = self.replaceTwoOrMore(w)
            #strip punctuation
            w = w.strip('\'"?,.')
            #check if it consists of only words
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]+[a-zA-Z0-9]*$", w)
            #ignore if it is a stopWord
            if(w in stopWords or val is None):
                continue
            else:
                featureVector.append(w.lower())
        return featureVector
    #end

    #start extract_features
    def extract_features(self, tweet):
        tweet_words = set(tweet)
        features = {}
        for word in self.featureList:
            features['contains(%s)' % word] = (word in tweet_words)
        return features
    #end

    def initNBClassifier(self, learningDataset):
      if os.path.isfile("NBClassifier.p"):
        self.NBClassifier = pickle.load(open( "NBClassifier.p", "rb" ) )
        print "Used ready!"
      else:
        inpTweets = csv.reader(open(learningDataset, 'rb'), delimiter=',', quotechar='"')
        count = 0;
        tweets = []
        for row in inpTweets:
            sentiment = row[0]
            tweet = row[1]
            processedTweet = self.processTweet(tweet)
            featureVector = self.getFeatureVector(processedTweet, self.stopWords)
            self.featureList.extend(featureVector)
            tweets.append((featureVector, sentiment));
        #end loop

        # Remove featureList duplicates
        self.featureList = list(set(self.featureList))

        # Generate the training set
        training_set = nltk.classify.util.apply_features(self.extract_features, tweets)

        # Train the Naive Bayes classifier
        self.NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

        # Saving the classifier
        pickle.dump(self.NBClassifier, open("NBClassifier.p", "wb"))
        print "Made A new one!"
    def classify(self, tweet):
      processedTweet = self.processTweet(tweet);
      sentiment = self.NBClassifier.classify(self.extract_features(self.getFeatureVector(processedTweet, self.stopWords)))
      return sentiment.strip('|')

#end class

# Test area for learning machine
#LM = TwitterLearningMachine('data/medium_size_dataset.csv')

#tweet = 'Bananas'
#print LM.classify(tweet)