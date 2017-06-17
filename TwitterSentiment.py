import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    def __init__(self):
        # read tokens
        with open("tokens.txt") as f:
            tokens = f.readlines()
        tokens = [x.strip() for x in tokens]
        print tokens
        consumer_key = tokens[0]
        consumer_secret = tokens[1]
        access_token = tokens[2]
        access_token_secret = tokens[3]

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("ERROR: Authentication Failed")
    
    def clean_tweet(self, tweet):
        # remove links and special characters
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def get_tweet_sentiment(self, tweet):
        # classify sentiment of tweet
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        
    def get_tweets(self, query, count = 10):
        # fetch and parse tweets
        tweets = []
        try:
            fetched_tweets = self.api.search(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepError as e:
            print("ERROR: " + str(e))

def main():
    # create TwitterClient object
    api = TwitterClient()
    count = 5000
    tweets = api.get_tweets(query = "#HuntRepublicanCongressman", count = count)
    pos_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    neg_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    neutral_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    print("{} tweets sampled".format(count))
    print("Percentage of positive sentiment tweets: {}%".format(100*len(pos_tweets)/len(tweets)))
    print("Percentage of negative sentiment tweets: {}%".format(100*len(neg_tweets)/len(tweets)))
    print("Percentage of neutral sentiment tweets: {}%".format(100*len(neutral_tweets)/len(tweets)))

if __name__ == "__main__":
    main()
