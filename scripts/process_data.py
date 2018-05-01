import pandas as pd
import datetime


def concat_data(coin, market_path, twitter_path):
    mh5 = pd.HDFStore(market_path)
    market_data = mh5['market']
    mh5.close()

    th5 = pd.HDFStore(twitter_path)
    tweet_data = th5['data']
    th5.close()

    data = pd.concat([tweet_data, market_data], axis=1)
    data.index = [datetime.datetime.fromtimestamp(d) for d in data.index]
    data = data.dropna(how='any')
    data_norm = (data - data.mean()) / (data.max() - data.min())

    store = pd.HDFStore('data/concat_data/' + coin + '.h5')
    store['data'] = data
    store['norm_data'] = data_norm
    store.close()


btc_market = './data/market_data/BTC-USD_data.h5'
eth_market = './data/market_data/ETH-USD_data.h5'
xrp_market = './data/market_data/XRP-USD_data.h5'
ltc_market = './data/market_data/LTC-USD_data.h5'

btc_twitter = './data/processed_data/bitcoin_tweets.h5'
eth_twitter = './data/processed_data/ethereum_tweets.h5'
xrp_twitter = './data/processed_data/ripple_tweets.h5'
ltc_twitter = './data/processed_data/litecoin_tweets.h5'

concat_data('bitcoin', btc_market, btc_twitter)
concat_data('ethereum', eth_market, eth_twitter)
concat_data('ripple', xrp_market, xrp_twitter)
concat_data('litecoin', ltc_market, ltc_twitter)
