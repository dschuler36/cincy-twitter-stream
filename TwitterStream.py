import tweepy
import json
import sqlite3
import apiConfig

# Twitter authentication stuff
global api
# API keys are stored in a separate file
access_token = apiConfig.access_token
access_token_secret = apiConfig.access_token_secret
consumer_key = apiConfig.consumer_key
consumer_secret = apiConfig.consumer_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# DB stuff
conn = sqlite3.connect('twitter.db')
c = conn.cursor()

# Class for defining a Tweet
class Tweet():

    # Data on the tweet
    def __init__(self, text, user, followers, date, location):
        self.text = text
        self.user = user
        self.followers = followers
        self.date = date
        self.location = location

    # Inserting that data into the DB
    def insertTweet(self):

        c.execute("INSERT INTO tweets (tweetText, user, followers, date, location) VALUES (?, ?, ?, ?, ?)",
            (self.text, self.user, self.followers, self.date, self.location))
        conn.commit()

# Stream Listener class
class TweetStreamListener(tweepy.StreamListener):

    # When data is received
    def on_data(self, data):

        # Error handling because teachers say to do this
        try:

            # Make it JSON
            tweet = json.loads(data)

            # filter out retweets
            if not tweet['retweeted'] and 'RT @' not in tweet['text']:

                # Get user via Tweepy so we can get their number of followers
                user_profile = api.get_user(tweet['user']['screen_name'])

                # assign all data to Tweet object
                tweet_data = Tweet(
                    str(tweet['text'].encode('utf-8')), # Have to use this encode because sometimes people tweet weird characters
                    tweet['user']['screen_name'],
                    user_profile.followers_count,
                    tweet['created_at'],
                    tweet['user']['location'])

                # Insert that data into the DB
                tweet_data.insertTweet()
                print("success")
        
        # Let me know if something bad happens            
        except Exception as e:
            print(e)
            pass

        return True

# Driver
if __name__ == '__main__':

    # Run the stream!
    l = TweetStreamListener()
    stream = tweepy.Stream(auth, l)

    # Filter the stream for these keywords. Add whatever you want here! 
    stream.filter(track=['Cincinnati', 'Cincy'])

