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

def crypto_buy_list(list, ammount, type):
	# Takes a list of cryptos and amount then outputs a list of orders to be executed
	orders = []
	if type == 'paper':
		url = paper_url
		headers = paper_headers
	elif type == 'live':
		url = live_url
		headers = live_headers
	else:
		print('Error, you must designate an account type with either paper or live')
	for i in list:
		order = {
		'symbol': i,
		'notional': ammount,
		'type': 'market',
		'side': 'buy',
		'time_in_force': 'gtc'
		}
		orders.append(order)
	return orders

