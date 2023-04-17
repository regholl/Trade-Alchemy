from dotenv import load_dotenv
import requests
import json
import os

'''
This file sets up the urls, endpoints and headers as well as structures all calls to the alpaca LIVE ACCOUNT api..

THE API CALLS HERE WILL AFFECT YOUR REAL MONEY ALPACA ACCOUNT
'''

#                                                       SETUP
#########################################################

url = 'https://api.alpaca.markets'
endpoints = {
        'account': '/v2/account',
        'orders': '/v2/orders',
        'positions': '/v2/positions'
             }

load_dotenv()
live_api = os.getenv("live_api")
live_secret = os.getenv("live_secret")
headers = {
 'Apca-Api-Key-Id': live_api,
 'Apca-Api-Secret-Key': live_secret
}


#                                                       LIVE ACCOUNT
#########################################################

def get_account():
	# Returns a dictionary containing live account details
	response = requests.get(url + endpoint['account'], headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving account. Status code: {response.status_code}')

