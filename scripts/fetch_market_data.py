import requests
import argparse
import pandas as pd

def get_historical_hourly_price(
        symbol,
        comparison_symbol,
        limit,
        aggregate,
        exchange=''):
    """
    Get the historical OHCL of a certain symbol pair for a certain
    exchange
    """
    url = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)

    if exchange:
        url += '&e={}'.format(exchange)

    page = requests.get(url)
    data = page.json()['Data']
    data_frame = pd.DataFrame(data)
    data_frame['mid'] = data_frame[["high", "low"]].mean(axis=1)
    data_frame = data_frame.set_index('time')
    return data_frame

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='Fetch data for analysis')

    parser.add_argument('--s1', type=str, required=True,
                        help='Symbol 1 of pair')
    parser.add_argument('--s2', type=str, required=True,
                        help='Symbol 2 of pair')
    parser.add_argument('--days', type=int, required=True,
                        help='number of days to fetch data')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    TIME_DELTA = 1

    hours = int(args.days) * 24

    file_name = args.s1 + '-' + args.s2 + '_data.h5'
    market_data = get_historical_hourly_price(args.s1, args.s2, hours, TIME_DELTA)

    store = pd.HDFStore('data/market_data/' + file_name)

    store['market'] = market_data  # save it
    print('Saved market data')


