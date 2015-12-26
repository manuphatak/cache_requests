#!/usr/bin/env python
# coding=utf-8
"""
Instructions:

.. code-block:: shell

    $ make install
    $ python examples/development_basics.py


Demonstrates requests are made once per unique arguments.

Sample output below.
"""

import logging

from cache_requests import Session

# setup log (used internally)
format_ = '%(relativeCreated)-5d %(name)-12s %(levelname)-8s %(message)s'
logging.basicConfig(level=logging.INFO, format=format_)

requests = Session(ex=15)  # 15 seconds, default: 60 minutes

# 1st unique call
response = requests.get('http://google.com')
response = requests.get('http://google.com')
response = requests.get('http://google.com')

headers = {
    "accept-encoding": "gzip, deflate, sdch",
    "accept-language": "en-US,en;q=0.8"
}
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


"""
Sample output
-------------

1st run:

.. code-block:: sh-session

    $ python examples/development_basics.py

    297   requests.packages.urllib3.connectionpool INFO     Starting new HTTP connection (1): google.com
    402   requests.packages.urllib3.connectionpool INFO     Starting new HTTP connection (1): www.google.com
    546   cache_requests.memoize INFO     Caching results for hash: 4cf379a8def12fe51f260ef0fe480221
    1022  cache_requests.memoize INFO     Caching results for hash: f8ac21842f69ea4fbb4bbbe92a0251a8
    <Response [200]>
    1704  cache_requests.memoize INFO     Caching results for hash: 940a5abb40af3bd1b9f73751f172bbf0
    <Response [200]>
    <Response [200]>
    <Response [200]>


2nd, 3rd..nth run (before 15s expiration):

.. code-block:: sh-session

    $ python examples/development_basics.py

    <Response [200]>
    <Response [200]>
    <Response [200]>
    <Response [200]>

After 15 seconds, it's back to the first result.
"""
