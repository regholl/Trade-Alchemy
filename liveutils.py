from methods import methods
import requests
'''This file pulls the urls, endpoints and headers from the methods file and structures all calls to the alpaca LIVE ACCOUNT api.. THE API CALLS HERE WILL AFFECT YOUR REAL MONEY ALPACA ACCOUNT'''

url = methods.urls['live']
endpoint = methods.endpoints
headers = methods.live_headers


def get_lv_account():
	# Returns a dictionary containing live account details
	response = requests.get(url + endpoint['account'], headers=headers)
	return reaponse.json()
