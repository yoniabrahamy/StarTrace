#import regex
import re
import csv
import pprint
import nltk.classify

import sys
#Change to your full local path, sorry currently it's the only way it works...
sys.path.insert(0, 'C:\Users\Johny\Documents\Final_Project\Twitter-Sentiment-Analyzer\libsvm\python')

import svm
from svmutil import *

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

#start process_tweet
def processTweet(tweet):
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
def getStopWordList(stopWordListFileName):
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
def getFeatureVector(tweet, stopWords):
    featureVector = []
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
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
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end

def getSVMFeatureVectorAndLabels(tweets, featureList):
    sortedFeatures = sorted(featureList)
    map = {}
    feature_vector = []
    labels = []
    for t in tweets:
        label = 0
        map = {}
        #Initialize empty map
        for w in sortedFeatures:
            map[w] = 0

        tweet_words = t[0]
        tweet_opinion = t[1]
        #Fill the map
        for word in tweet_words:
            #process the word (remove repetitions and punctuations)
            word = replaceTwoOrMore(word)
            word = word.strip('\'"?,.')
            #set map[word] to 1 if word exists
            if word in map:
                map[word] = 1
        #end for loop
        values = map.values()
        feature_vector.append(values)
        if(tweet_opinion == 'positive'):
            label = 0
        elif(tweet_opinion == 'negative'):
            label = 1
        elif(tweet_opinion == 'neutral'):
            label = 2
        labels.append(label)
    #return the list of feature_vector and labels
    return {'feature_vector' : feature_vector, 'labels': labels}
#end

#JA: This one i wrote by myself
def getSVMFeatureVector(testTweets, featureList):
    sortedFeatures = sorted(featureList)
    map = {}
    feature_vector = []
    for t in tweets:
        map = {}
        #Initialize empty map
        for w in sortedFeatures:
            map[w] = 0

        tweet_words = t[0]
        #Fill the map
        for word in tweet_words:
            #process the word (remove repetitions and punctuations)
            word = replaceTwoOrMore(word)
            word = word.strip('\'"?,.')
            #set map[word] to 1 if word exists
            if word in map:
                map[word] = 1
        #end for loop
        values = map.values()
        feature_vector.append(values)

    #return the list of feature_vector
    return feature_vector
#end

#Read the tweets one by one and process it
inpTweets = csv.reader(open('data/sampleTweets.csv', 'rb'), delimiter=',', quotechar='"')
stopWords = getStopWordList('data/feature_list/stopwords.txt')
count = 0;
featureList = []
tweets = []
for row in inpTweets:
    sentiment = row[0]
    tweet = row[1]
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet, stopWords)
    featureList.extend(featureVector)
    tweets.append((featureVector, sentiment));
#end loop

# Remove featureList duplicates
featureList = list(set(featureList))

# Generate the training set
training_set = nltk.classify.util.apply_features(extract_features, tweets)

# Train the Naive Bayes classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)


#Train the SVM classifier
#result = getSVMFeatureVectorAndLabels(tweets, featureList)
#problem = svm_problem(result['labels'], result['feature_vector'])
#'-q' option suppress console output
#param = svm_parameter('-q')
#param.kernel_type = LINEAR
#classifier = svm_train(problem, param)
#svm_save_model('TestClassifer', classifier)


#Test the svm classifier

#testTweet = 'The sun is shining brightly, such a wonderful day!'
#shittyTweet = 'My mouth really hurts. It makes me feel sad'
#processedTestTweet = processTweet(testTweet)
#processedShitTestTweet = processTweet(shittyTweet)

#print processedTestTweet
#print processedShitTestTweet

#test_feature_vector = getSVMFeatureVector(processedTestTweet, featureList)
#bad_test_feature_vector = getSVMFeatureVector(processedShitTestTweet, featureList)

#p_labels contains the final labeling result
#p_labels, p_accs, p_vals = svm_predict([0] * len(test_feature_vector),test_feature_vector, classifier)
#p2_labels, p2_accs, p2_vals = svm_predict([0] * len(bad_test_feature_vector),bad_test_feature_vector, classifier)

#print "Acording to svm test:"
#print "Good Tweet: %s, sentiment=%s\n" % (testTweet, p_labels);
#print "Bad Tweet: %s, sentiment=%s\n" % (shittyTweet, p2_labels);

# Test the naive bayes classifier
testTweet = 'Wow so much love, perfect and delight'
shittyTweet = 'My mouth really hurts. It makes me feel sad'
processedTestTweet = processTweet(testTweet)
processedShitTestTweet = processTweet(shittyTweet)
sentiment = NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet, stopWords)))
badsentiment = NBClassifier.classify(extract_features(getFeatureVector(processedShitTestTweet, stopWords)))

print "Acording to Naive bayse:"
print "testTweet = %s, sentiment = %s\n" % (testTweet, sentiment)
print "testShittyTweet = %s, sentiment = %s\n" % (shittyTweet, badsentiment)
