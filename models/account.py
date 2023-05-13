from dotenv import load_dotenv
import datetime
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

def get_account(type):
	if type == 'paper':
		response = requests.get(
		paper_url + endpoint['account'],
		headers=paper_headers)
	elif type == 'live':
		response = requests.get(
		live_url + endpoint['account'],
		headers=live_headers)
	else:
		print('You must provide a proper account type (paper/live) in order to return a value!')
		return
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving account details. Status code: {response.status_code}. Message: {response.content}')
		
		
def get_activities(type):
	if type == 'paper':
		response = requests.get(
		paper_url + endpoint['activity'],
		headers=paper_headers)
	elif type == 'live':
		response = requests.get(
		live_url + endpoint['activity'],
		headers=live_headers)
	else:
		print('You must provide a proper account type (paper/live) in order to return a value!')
		return
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving activities. Status code: {response.status_code}. Message: {response.content}')


def get_watchlist(type):
	if type == 'paper':
		response = requests.get(paper_url + endpoint['watchlist'], headers=paper_headers)
	elif type == 'live':
		response = requests.get(live_url + endpoint['watchlist'], headers=live_headers)
	else:
		print('You must provide a proper account type (paper/live) in order to return a value!')
		return
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retreiving watchlists. Status code: {response.status_code}. Message: {response.content}')
		
		
def market_status():
	# Gets the current market status as a boolean
	status = None
	response = requests.get(live_url + endpoint['clock'], headers=live_headers)
	if response.status_code != 200:
		raise ValueError('Failed to retrieve market status')
	market_status = response.json()['is_open']
	if market_status:
		status = True
	else:
		status = False
	return status
	
	
def get_cash(type):
	# Returns available cash for the account
	cash = get_account(type)['cash']
	return cash
