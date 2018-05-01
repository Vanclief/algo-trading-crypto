import re
import yaml
import calendar
import pandas as pd

from pathlib import Path
from datetime import datetime
from influxdb import InfluxDBClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# VADER
analyzer = SentimentIntensityAnalyzer()

# InfluxDB connections settings
host = 'XXX.XXX.XXX.XXX'
port = XXX
user = 'XXX'
password = 'XXX'
dbname = 'cryptotweets'
metric = 'tweets'

client = InfluxDBClient(host, port, user, password, dbname)


def create_filters(config):
    filters = {}

    topics = config['topics']
    for key, keywords in topics.items():
        regex = []
        for keyword in keywords:
            regex.append(re.escape(keyword) + r'\b')

        filters[key] = regex

    return filters


def process_tweets(raw_tweets, filters):

    tweets = {}

    for key, _ in filters.items():
        tweets[key] = []

    for response in raw_tweets:
        for tweet in response:

            if not tweet:
                break

            time = calendar.timegm(datetime.strptime(
                tweet['time'][:19], "%Y-%m-%dT%H:%M:%S").timetuple())

            polarity = analyzer.polarity_scores(tweet['text'])

            new_t = {
                'time': time,
                'neg': polarity['neg'],
                'neu': polarity['neu'],
                'pos': polarity['pos'],
                'norm': polarity['compound']
                }

            for key, keywords in filters.items():
                regex = '|'.join(map(str, keywords))

                if re.search(regex, tweet['text']):
                    tweets[key].append(new_t)

    return tweets


def fetch_tweets(start_time, end_time):

    with open('config.yml', 'r') as config_file:
        config = yaml.load(config_file)

    start_date = pd.to_datetime(start_time, unit='s')
    end_date = pd.to_datetime(end_time, unit='s')

    path = 'data/twitter_data/' + str(start_date)[:10] + "_" + \
           str(end_date)[:10] + '.h5'

    print("Looking for tweets between " + str(start_date) + " and " +
          str(end_date))

    if Path(path).is_file():
        print("Cached data found: There is already data for that timeframe")
        return True

    print("No cached data found: Fetching data for that timeframe")

    filters = create_filters(config)

    query = "SELECT * FROM {} WHERE time > '{}' and time < '{}'".format(
            metric, str(start_date)[:10], str(end_date)[:10])

    raw_tweets = client.query(query, database=dbname, chunked=True)

    print('Processing tweets')

    tweets = process_tweets(raw_tweets, filters)

    store = pd.HDFStore(path)

    topics = config['topics']

    for topic in topics:
        if tweets[topic]:
            dataframe = pd.DataFrame(tweets[topic])
            dataframe = dataframe.set_index('time')
            save_name = topic + '_tweets'
            store[save_name] = dataframe
            print('Saved: ' + save_name)

    store.close()
    print('Done')
    return True
