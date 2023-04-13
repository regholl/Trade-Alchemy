from methods import methods
import requests
'''This file pulls the urls, endpoints and headers from the methods file and structures all calls to the alpaca LIVE ACCOUNT api.. THE API CALLS HERE WILL AFFECT YOUR REAL MONEY ALPACA ACCOUNT'''

urls = methods.urls
endpoints = methods.endpoints
headers = methods.live_headers


def get_lv_account():
	# Returns a dictionary containing live account details
	response = requests.get(urls['live'] + endpoints['account'], headers=headers)
	account = response.json()
	return account
