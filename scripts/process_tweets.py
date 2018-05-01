import os
import pandas as pd
import numpy

tweets_path = './data/twitter_data/'
processed_path = './data/processed_data/'
files = os.listdir(tweets_path)


def process(store, category):
    df = store[category]
    df = resample(df)
    df = calculate_polarity(df)
    return df


def resample(df):
    df.index = [(t//3600) * 3600 for t in df.index]
    df = df.groupby(df.index).mean()
    return df


def calculate_polarity(df):
    df['pol'] = numpy.sqrt(df['pos'] * df['neg'])
    return df


def save_data(df, category):
    store = pd.HDFStore(processed_path + category + '.h5')
    store['data'] = df
    store.close()


btc = pd.DataFrame()
eth = pd.DataFrame()
xrp = pd.DataFrame()
ltc = pd.DataFrame()

for f in files:
    store = pd.HDFStore(tweets_path + f)
    btc = pd.concat([btc, (process(store, 'bitcoin_tweets'))])
    eth = pd.concat([eth, (process(store, 'ethereum_tweets'))])
    xrp = pd.concat([xrp, (process(store, 'ripple_tweets'))])
    ltc = pd.concat([ltc, (process(store, 'litecoin_tweets'))])
    store.close()

save_data(btc, 'bitcoin_tweets')
save_data(eth, 'ethereum_tweets')
save_data(xrp, 'ripple_tweets')
save_data(ltc, 'litecoin_tweets')
