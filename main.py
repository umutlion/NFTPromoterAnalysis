import pandas as pd
import tweepy

def scrape(words, date_since, numtweet):
    db = pd.DataFrame(columns=['username', 'description', 'location', 'following',
                               'followers', 'totaltweets', 'retweetcount', 'text', 'hashtags'])

    tweets = tweepy.Cursor(api.search_tweets, q=words, lang="en", since=date_since, tweet_mode='extended').items(numtweet)

    list_tweets = [tweet for tweet in tweets]
    i = 1

    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        retweetcount = tweet.retweet_count
        hashtags = tweet.entities['hashtags']
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])

        ith_tweet = [username, description, location, following,
                     followers, totaltweets, retweetcount, text, hashtext]
        db.loc[len(db)] = ith_tweet

        i = i + 1
    filename = 'scraped_tweets.csv'

    db.to_csv(filename)


if __name__ == '__main__':
    consumer_key = "yB8GV2Qqofa4iKfhR7JVEAWHq"
    consumer_secret = "ltwuIyMdNjQe6bqLuIJVaCdqXNp5FSL1VPul1NiRMSrdM6zkhu"
    access_key = "353460411-G8ggU0Pe7CplI22y1UbVPQVu2fyZ0sVfP6aVKC29"
    access_secret = "qGrMLWPvS8GMd1MvKueLPRM9v7zCf80PwWKRHwhClAITs"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    print("Enter Twitter HashTag to search for")
    words = input()
    print("Enter Date since The Tweets are required in yyyy-mm--dd")
    date_since = input()

    numtweet = 100
    scrape(words, date_since, numtweet)
    print('Scraping has completed!')

