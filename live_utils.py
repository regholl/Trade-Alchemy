import methods
import requests
import json 

'''This file pulls the urls, endpoints and headers from the methods file and structures all calls to the alpaca LIVE ACCOUNT api.. THE API CALLS HERE WILL AFFECT YOUR REAL MONEY ALPACA ACCOUNT'''

url = methods.urls['live']
endpoint = methods.endpoints
headers = methods.live_headers


def get_account():
	# Returns a dictionary containing live account details
	response = requests.get(url + endpoint['account'], headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving account. Status code: {response.status_code}')
