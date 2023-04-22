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

endpoint = {
        'account': '/v2/account',
        'orders': '/v2/orders',
        'positions': '/v2/positions',
        'activity': '/v2/account/activities',
        'assets': '/v2/assets'
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
	# Returns a dictionary containing paper account details
	response = requests.get(url + endpoint['account'], headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving account. Status code: {response.status_code}')
		
		
def get_positions():
	# Returns a list of all open positions
	response = requests.get(url + endpoint['positions'], headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving positions. Status code: {response.status_code}')
		
		
def get_orders():
	# Returns a list of ALL open orders
	response = requests.get(url + endpoint['orders'], headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving orders. Status code: {response.status_code}')
		
		
def get_order_by_id(id):
	# Returns details of the order id that is passed in
	response = requests.get(url + endpoint['orders'] + f"/{id}", headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving order. Status code: {response.status_code}')
		
		
def post_order(order):
	# Accepts a dict object and returns order details
	response = requests.post(url + endpoint['orders'],
	headers=headers, json=order)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error placing order. Status code: {response.status_code}')
		
		
def get_activity():
	# Returns a list of all account activity
	response = requests.get(url + endpoint['activity'], headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving the requested activity. Status code: {response.status_code}')
		
		
def close_all_positions():
	# Send a DELETE request to close all positions
	response = requests.delete(url + endpoint['positions'], headers=headers)
	if response.status_code == 207:
		print("All positions have been closed.")
	else:
		print(f"Error while closing positions. Status code:{response.text}")


def get_negative_pnl():
	# Paper accoount dollar cost average. This routine checks all positions for negative PNL and returns them in a list
	# Gather account and position informatikn
	account_info = pa.get_account()
	portfolio_value = float(account_info['portfolio_value'])
	positions = pa.get_positions()
	# Create list of assets with higher average buy price than current price
	underwater_assets = []
	for position in positions:
		asset_symbol = position['symbol']
		avg_entry_price = float(position['avg_entry_price'])
		current_price = float(position['current_price'])
		if avg_entry_price > current_price:
			underwater_assets.append(asset_symbol)
	# Return list of assets with higher average buy price than current price
	if len(underwater_assets) > 0:
		print("The following assets in your portfolio have a higher average buy price than current price:")
		return underwater_assets
	else:
		print("All assets in your portfolio have a lower or equal average buy price than current price.")
