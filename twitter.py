#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from requests_oauthlib import OAuth1
import urllib
import time
from collections import Counter
import sys
import operator

import text

__author__ = 'Mauricio Quezada'
__email__ = 'mquezada@dcc.uchile.cl'
__twitter__ = '@waxkun'


API_KEY = 'OAj6thblBFmC6u19h9YA'
API_SECRET = 'BH2ANmo1cfIpteYhjZ3Ux3jJhmvxjIeunEQniVs4nk'
USER_TOKEN = '1529430332-UPKUtqtgujcPNwmAaJKN6oUNmVRuuw7iyy7QfZt'
USER_SECRET = 'CsSrccu9OvlCmJHhbaF1z54veelkvBK5lE3k95K0'

auth = OAuth1(API_KEY, API_SECRET, USER_TOKEN, USER_SECRET)


def unshorten_url(url, timeout=5):
    try:
        return requests.request('HEAD', url, timeout=timeout).url
    except:
        return url


def get_tweet(id=None):
    # 347567103089467392
    url = 'https://api.twitter.com/1.1/statuses/show.json?id=' + id
    response = requests.get(url, auth=auth)

    return response


def _search_tweets(keywords=[], count=3, params={}):
    if not params:
        twitter_params = {
            'q': ' OR '.join(keywords),
            'count': count,
        }
    else:
        twitter_params = params

    url = 'https://api.twitter.com/1.1/search/tweets.json?'
    search_url = url + urllib.urlencode(twitter_params)
    response = requests.get(search_url, auth=auth)

    return response


def search_tweets2(keywords=[], count=3):
    params = {}
    while True:
        try:
            response = _search_tweets(keywords, count, params)
            if response.ok:
                js = response.json()
                yield js

                params = {
                    'q': ' OR '.join(keywords),
                    'count': count,
                    'since_id': js['search_metadata']['max_id']
                }
            else:
                print response.content

            time.sleep(5)
        except KeyboardInterrupt:
            break


def texts_from_search(keywords=[], count=3):
    for result in search_tweets2(keywords, count):
        for status in result['statuses']:
            yield status['text']


if __name__ == '__main__':
    """ejemplo de juguete, imprime el estado actual de un counter con las palabras
    mas frecuentes de los tweets obtenidos hasta el momento.

    modo de uso:
    python twitter.py <count> <keywords>...

    ejemplo:
    python twitter.py 100 obama prism nsa
    """
    c = Counter()
    count = sys.argv[1]
    keywords = sys.argv[2:]
    for tweet in texts_from_search(keywords, count):
        clean_text = text.clean_words(tweet)
        for word in [words for words in clean_text if words not in keywords]:
            c[word] += 1
        print map(operator.itemgetter(0), c.most_common(10))
