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

def get_orders(type):
	# Returns a list of ALL open orders
	if type == 'paper':
		response = requests.get(
		paper_url + endpoint['orders'], headers=paper_headers)
	elif type == 'live':
		response = requests.get(
		live_url + endpoint['orders'], headers=live_headers)
	else:
		print('You must provide a proper account type (paper/live) in order to return a value!')
		return
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving orders. Status code: {response.status_code}. Message: {response.content}')
		
		
def get_order_by_id(type, id):
	# Returns details of the order id that is passed in
	if type == 'paper':
		response = requests.get(
		paper_url + endpoint['orders'] + f"/{id}", headers=paper_headers)
	elif type == 'live':
		response = requests.get(
		live_url + endpoint['orders'], headers=live_headers)
	else:
		print('You must provide a proper account type (paper/live) in order to return a value!')
		return
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving order. Status code: {response.status_code}. Message: {response.content}')
		
		
def post_order(type, order):
	# Accepts a dict object and returns order details
	if type == 'paper':
		response = requests.post(
		paper_url + endpoint['orders'],
		headers=paper_headers,
		json=order)
	elif type == 'live':
		response = requests.post(
		live_url + endpoint['orders'],
		headers=live_headers,
		json=data)
	else:
		print('You must provide a proper account type (paper/live) in order to return a value!')
		return
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error placing order. Status code: {response.status_code}. Message: {response.content}')

