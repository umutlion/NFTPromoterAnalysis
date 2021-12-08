import tweepy
import json
import re
import mysql.connector as sqlcon
import time
import datetime
import pandas as pd

while True:
    if datetime.datetime.now().minute % 5 == 0:


        conn = sqlcon.connect(
            host = "localhost",
            user = "root",
            password = "password",
            database = "Twitter",
            auth_plugin='mysql_native_password',
            port = 3306)

        c = conn.cursor()


        twitter_username_re = re.compile(r'@([^\s:]+)')
        dummy = []

        class StreamListener(tweepy.Stream):
            def on_status(self, status):
                print(status)

            def on_error(self, status_code):
                print(status_code)

            def on_data(self, data):
                all_data = json.loads(data)
                created_at = pd.to_datetime(all_data['created_at'])
                favorite_count = all_data['favorite_count']
                favorited = all_data['favorited']
                filter_level = all_data['filter_level']
                lang = all_data['lang']
                retweet_count = all_data['retweet_count']
                retweeted = all_data['retweeted']
                source = all_data['source']
                text = all_data['text']

                dummy.append(all_data['text'])
                for x in dummy:
                    taggedusers = []
                    x = twitter_username_re.findall(x)
                    taggedusers.append(x)

                tagged = " ".join('%s' %id for id in taggedusers)

                truncated = all_data['truncated']
                user_created_at = all_data['user']['created_at']
                user_followers_count = all_data['user']['followers_count']
                user_location = all_data['user']['location']
                user_lang = all_data['user']['lang']
                user_name = all_data['user']['name']
                user_screen_name = all_data['user']['screen_name']
                user_time_zone = all_data['user']['time_zone']
                user_utc_offset = all_data['user']['utc_offset']
                user_friends_count = all_data['user']['friends_count']

                q=('''INSERT INTO tweets4
                            (created_at, favorite_count, favorited, filter_level, lang, retweet_count,
                            retweeted, source, text, tagged, truncated, user_created_at, user_followers_count,
                            user_location, user_lang, user_name, user_screen_name, user_time_zone,
                            user_utc_offset, user_friends_count)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''')

                results = (created_at, favorite_count, favorited, filter_level, lang, retweet_count,
                           retweeted, source, text, tagged, truncated, user_created_at, user_followers_count,
                           user_location, user_lang, user_name, user_screen_name, user_time_zone,
                           user_utc_offset, user_friends_count)

                c.execute(q, results)

                conn.commit()


        consumer_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        access_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        access_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)

        api = tweepy.API(auth)

        stream_listener = StreamListener(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_key, access_token_secret=access_secret)

        stream_listener.filter(track=["#NFTGiveaways"], languages=['en'])

        conn.close()

        time.sleep(60)


