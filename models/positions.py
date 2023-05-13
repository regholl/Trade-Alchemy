from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

# Live Config
########################################################

live_url = 'https://api.alpaca.markets'
live_api = os.getenv("live_api")
live_secret = os.getenv("live_secret")
live_headers = {
 'Apca-Api-Key-Id': live_api,
 'Apca-Api-Secret-Key': live_secret
}

# Paper Config
#########################################################

paper_url = 'https://paper-api.alpaca.markets'
paper_api = os.getenv("paper_api")
paper_secret = os.getenv("paper_secret")
paper_headers = {
 'Apca-Api-Key-Id': paper_api,
 'Apca-Api-Secret-Key': paper_secret
}

# Common Endpoints
#########################################################

endpoint = {
        'account': '/v2/account',
        'orders': '/v2/orders',
        'positions': '/v2/positions',
        'activity': '/v2/account/activities',
        'assets': '/v2/assets',
        'watchlist': '/v2/watchlists',
        'clock': '/v2/clock'
             }

# Methods
#########################################################


def get_all_positions(type):
	target = endpoint['positions']
	if type == 'paper':
		url = paper_url
		headers = paper_headers
	elif type == 'live':
		url = live_url
		headers = live_headers
	else:
		print('You must provide a proper account type (paper/live) in order to return a value!')
		return
	response = requests.get(url + target, headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving positions. Status code: {response.status_code}. Message: {response.content}')
		
		
def close_all_positions(type):
	target = endpoint['positions']
	if type == 'paper':
		url = paper_url
		headers = paper_headers
	elif type == 'live':
		url = live_url
		headers = live_headers
	else:
		print('You must provide a proper account type (paper/live) in order to return a value!')
		return
	response = requests.delete(url + target, headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	elif response.status_code == 207:
		data = json.loads(response.content)
		print('Error, there are no positions capabale of being closed')
	else:
		print(f'Error closing positions. Status code: {response.status_code}. Message: {response.content}')
