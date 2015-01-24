import json
import sys
import urllib
import urllib2
import oauth2

#code taken from https://github.com/Yelp/yelp-api/blob/master/v2/python/sample.py

url = 'http://api.yelp.com/v2/search/?'
DEFAULT_TERM = 'lunch'
DEFAULT_LOCATION = 'New York City, NY'
SEARCH_LIMIT = 3


CONSUMER_KEY = "UggI6CZTqoXNSvFUzZiC0Q"
CONSUMER_SECRET = "C6-GZLE0-2lGbvaT7mN7uHqUODQ"
TOKEN = "lcLATmucVPk-4YyjHCNec6AgJJ7CabLl"
TOKEN_SECRET = "8naFSi_ZknAav9_KSWg6rtHvvVg"

def request(url_params):
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)
    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
        conn.close()
    except:
        response = {}
    return response

def search(term, location):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(url_params)

