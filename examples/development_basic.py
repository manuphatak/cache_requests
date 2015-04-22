#!/usr/bin/env python
# coding=utf-8
import logging
from cache_requests import requests, config

config.EXPIRATION = 15
config.REDISLITE_DB = 'redis/requests.redislite'

format_ = '%(relativeCreated)-5d %(name)-12s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=format_)


format_ = '%(relativeCreated)-5d %(name)-12s %(levelname)-8s %(message)s'
# 1st unique call
response = requests.get('http://google.com')
response = requests.get('http://google.com')
response = requests.get('http://google.com')

headers = {"accept-encoding": "gzip, deflate, sdch", "accept-language": "en-US,en;q=0.8"}
payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8", client="ubuntu",
               q="hash%20a%20dictionary%20python")
# 2nd unique call
response = requests.get('http://google.com/search', headers=headers, params=payload)
response = requests.get('http://google.com/search', headers=headers, params=payload)
response = requests.get('http://google.com/search', headers=headers, params=payload)
response = requests.get('http://google.com/search', headers=headers, params=payload)
response = requests.get('http://google.com/search', headers=headers, params=payload)

print(response)
payload = dict(sourceid="chrome-instant", ion="1", espv="2", ie="UTF-8", client="ubuntu",
               q="hash%20a%20dictionary%20python2")
# 3rd unique call
response = requests.get('http://google.com/search', headers=headers, params=payload)
response = requests.get('http://google.com/search', headers=headers, params=payload)

print(response)
print(response)
print(response)

# Pay attention to the number of requests made.   Even though there are 10
# `requests.get`s, there's only 3 requests being sent out.

# Now run it again within 15 seconds.

# This time there was 0 unique `requests.get`s.  It pulls 100% from cache.

# Wait 15 seconds, and run it one last time.  Now that those keys have expired it
# will resend those requests and repopulate the cache storage.

# One more thing, you may notice.  It runs almost 10x faster when it's not sending
# requests.