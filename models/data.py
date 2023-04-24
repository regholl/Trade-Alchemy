from dotenv import load_dotenv
from datetime import datetime
import requests
import json
import os

'''
This file sets up all the necessary tooling to query the market data endpoints. Most endpoints are symbol specific so they cant be stored as a separate dict but rather used in the functions themselves.
'''

#                                                       SETUP
#########################################################

url = 'https://data.alpaca.markets/v2/stocks'
crypto_url = 'https://data.alpaca.markets/v1beta3/crypto'
crypto_endpoints = {
        'quotes': '/us/latest/quotes',
        'bars': '/us/bars'
}

load_dotenv()
live_api = os.getenv("live_api")
live_secret = os.getenv("live_secret")
headers = {
 'Apca-Api-Key-Id': live_api,
 'Apca-Api-Secret-Key': live_secret
}

#                                                       STOCK DATA
#########################################################

def get_stock_snapshot(symbol):
	# Returns most recent details of the symbol passed in
	endpoint = f'/{symbol}/snapshot'
	response = requests.get(url + endpoint, headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving snapshot for {symbol}. Status code: {response.status_code}')
		
		
def get_stock_spread(symbol):
	# Returns a dictionary of the current bid/ask spread
	snapshot = get_stock_snapshot(symbol)
	latest_quote = snapshot['latestQuote']
	ask = latest_quote['ap']
	bid = latest_quote['bp']
	spread = {'ask': ask, 'bid':bid}
	return spread
	
	
#                                                       CRYPTO DATA
#########################################################

def get_crypto_quote(symbol):
	# Returns current quote for symbol passed in
	url = crypto_url
	endpoint = crypto_endpoints['quotes']
	data = {'symbols':symbol}
	response = requests.get(url + endpoint, params=data, headers=headers)
	if response.status_code == 200:
		quote = json.loads(response.content)
		return quote
	else:
		print(f'Error retrieving quote for {symbol}. Status code: {response.status_code}')
		
		
def get_crypto_spread(symbol):
	# Returns the spread prices feom a quote
	quote = get_crypto_quote(symbol)
	ask = float(quote['quotes'][symbol]['ap'])
	bid = float(quote['quotes'][symbol]['bp'])
	median = {'ask': ask, 'bid': bid}
	return spread
	
	
def get_crypto_bars(symbol, timeframe, start=None, end=None, limit=None):
	# Returns a bars object for the specified symbol
	url = crypto_url
	endpoint = crypto_endpoints['bars']
	data = {
	'symbols':symbol,
	'timeframe':timeframe,
	'start': start,
	'end': end,
	'limit': limit
	}
	response = requests.get(url + endpoint, params=data, headers=headers)
	if response.status_code == 200:
		bars = json.loads(response.content)
		return bars
	else:
		print(f'Error retrieving bars for {symbol}. Status code: {response.status_code}{response.content}')

