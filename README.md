
# Algo-Trading-Crypto

This is a complementary repository for [this paper](https://github.com/Vanclief/algo-trading-crypto/blob/master/fv_ag-atcsaml.pdf). We include our dataset
alongside the scripts that where used for its creation. This study was done for
the Bitcoin, Ethereum, Litecoin and Ripple cryptocurrencies. However you can run 
the scripts yourself to collect data from any desired cryptocurrency. 
Machine Learning models where implemented using the 
[Sci-kit](http://scikit-learn.org/stable/index.html) library.

## Dependencies

* Python 3+

* InfluxDB

* Redis

**Recomended**

* Jupyter Notebook

## Setup

You can play with the provided datasets. If you want to collect your own data
you can use the *fetch_market_data.py* script and 
[Tweet-catcher](https://github.com/Vanclief/tweet-catcher).

## Datasets

Datasets are included under the data folder in .h5 format. 


## Scripts

Processing scripts are contained inside the _scripts_ folder.

* `fetch_market_data.py --s1 LTC --s2 USD --days 80` - Gets data from now since 
  the specified number of days for the symbol pair.

* `fetcher.py --days 60` - Creates a queue for obtaining tweets from now since the 
  specified number of days. You need to run a worker instance.

* `process_tweets.py` - Applies VADER lexicon to the tweets

* `process_data.py` - Concatenates the market and twitter data into a single
  dataset

