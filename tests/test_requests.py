#!/usr/bin/env python
# coding=utf-8
from pytest import fixture



@fixture
def requests():
    from cache_requests import requests as r, Config

    Config.ex = 1
    Config.dbfilename = 'redis/requests.redislite'

    return r

def test_requests_properly_patched()

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
