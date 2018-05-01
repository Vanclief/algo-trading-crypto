import os
import time
import argparse
import calendar

from datetime import datetime
from rq import Connection, Queue
from fetch_tweets import fetch_tweets
from redis import Redis


def main(nb_day):

    now = datetime.utcnow().date()
    today = calendar.timegm(now.timetuple())

    async_results = {}
    q = Queue()
    for x in range(0, nb_day):
        end_date = today - ((x+1) * 86400)
        start_date = end_date - 86400

        async_results[x] = q.enqueue(fetch_tweets, start_date, end_date,
                                     timeout='2h')

    start_time = time.time()
    done = False

    while not done:
        os.system('clear')
        print('Asynchronously: (time = %.2f)' % (time.time() - start_time,))
        done = True
        for x in range(0, nb_day):
            result = async_results[x].return_value
            if result is None:
                done = False
                result = '(WIP)'
            print('Tweets from (%d) day before today = %s' % (x+1, result))
        time.sleep(0.2)

    print('Done')


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='Fetch data for analysis')
    parser.add_argument('--days', type=int, required=True,
                        help='number of days to fetch data')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    with Connection(Redis('localhost', 6379)):
        main(nb_day=args.days)
