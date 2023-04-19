import matplotlib.pyplot as plt
from dotenv import load_dotenv
import models.paper as pa
import models.data as dt
import requests
import time
import math
import os

def gridbot1():
	load_dotenv()
	API_KEY = os.getenv('paper_api')
	API_SECRET = os.getenv('paper_secret')
	APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
	headers = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET}
	
	max_invested = 0.1  # BTC
	grid_spacing = 0.005  # $5
	
	# State variables
	invested = 0
	buys = []
	sells = []
	profit = 0
	
	while True:
		# Get current BTC price
		r = requests.get(f'{APCA_API_BASE_URL}/v2/stocks/BTC/trades/latest',
		headers=headers)
		btc_price = float(r.json()[0]['p'])
		
		# If no buys/sells yet, place initial buy order
		if not buys and not sells:
			qty = max_invested / btc_price
			r = requests.post(f'{APCA_API_BASE_URL}/v2/orders',
			headers=headers,
			json={'symbol': 'BTC', 'qty': qty, 'side': 'buy', 'type': 'market', 'time_in_force': 'day'})
			buys.append(r.json())
			invested += qty
			continue
			
		# Adjust grids if price changed
		if btc_price != buys[-1]['average_fill_price'] or btc_price != sells[-1]['average_fill_price']:
			buys = [b for b in buys if b['average_fill_price'] < btc_price]
			sells = [s for s in sells if s['average_fill_price'] > btc_price]
			if not buys or btc_price - buys[-1]['average_fill_price'] > grid_spacing:
				qty = max_invested / btc_price - invested
				r = requests.post(f'{APCA_API_BASE_URL}/v2/orders',
				headers=headers,
				json={'symbol': 'BTC', 'qty': qty, 'side': 'buy', 'type': 'market', 'time_in_force': 'day'})
				buys.append(r.json())
			if not sells or sells[-1]['average_fill_price'] - btc_price > grid_spacing:
				qty = invested - max_invested / btc_price
				r = requests.post(f'{APCA_API_BASE_URL}/v2/orders',
				headers=headers,
				json={'symbol': 'BTC', 'qty': qty, 'side': 'sell', 'type': 'market', 'time_in_force': 'day'})
				sells.append(r.json())
				
		# Update state
		buys = [b for b in buys if b['status'] != 'filled']
		sells = [s for s in sells if s['status'] != 'filled']
		r = requests.get(f'{APCA_API_BASE_URL}/v2/account',
		headers=headers)
		invested = float(r.json()['BTC']['qty'])
		profit = float(r.json()['USD']['cash'])
		
		# Sleep and repeat
		time.sleep(1)

#########################################################

def gridbot2():
	load_dotenv()
	API_KEY = os.getenv('paper_api')
	SECRET_KEY = os.getenv('paper_secret')
	ENDPOINT = 'https://paper-api.alpaca.markets'
	
	# Set up trading parameters
	SYMBOL = 'BTCUSD'
	GRID_SIZE_PERCENT = 2 # Grid size as a percentage of current price
	NUM_GRIDS = 10 # Number of buy and sell grids on each side of current price
	MAX_INVESTED = 1000 # Maximum amount to invest in USD
	BUY_SELL_DELAY = 10 # Time in seconds between placing buy and sell orders
	PLOT_DELAY = 2 # Time in seconds between refreshing plot
	
	# Set up Alpaca API headers
	headers = {
	'APCA-API-KEY-ID': API_KEY,
	'APCA-API-SECRET-KEY': SECRET_KEY
	}
	
	# Initialize global variables
	current_price = None
	buy_grids = []
	sell_grids = []
	buy_orders = []
	sell_orders = []
	total_profit = 0
	pl_history = [0]
	time_history = [time.time()]
	
	# Functions for placing and cancelling orders
	def place_order(side, qty, price):
		data = {
		'symbol': SYMBOL,
		'qty': qty,
		'side': side,
		'type': 'limit',
		'time_in_force': 'gtc',
		'limit_price': price
		}
		r = requests.post(f'{ENDPOINT}/v2/orders', json=data, headers=headers)
		return r.json()
		
	def cancel_order(order_id):
		r = requests.delete(f'{ENDPOINT}/v2/orders/{order_id}', headers=headers)
		return r.json()
		
	# Function for computing grid prices
	def compute_grids():
		global current_price, buy_grids, sell_grids
		if current_price is None:
			return
		grid_size = current_price * GRID_SIZE_PERCENT / 100
		buy_grids = [current_price - (i+1) * grid_size for i in range(NUM_GRIDS)]
		sell_grids = [current_price + (i+1) * grid_size for i in range(NUM_GRIDS)]
		
	# Function for placing buy and sell orders
	def place_orders():
		global buy_orders, sell_orders
		buy_orders = []
		sell_orders = []
		for i in range(NUM_GRIDS):
			if i < len(buy_grids) and sum([o['side']=='buy' for o in buy_orders]) * GRID_SIZE_PERCENT / 100 < MAX_INVESTED:
				qty = math.floor(MAX_INVESTED / buy_grids[i])
				buy_orders.append(place_order('buy', qty, buy_grids[i])['id'])
			if i < len(sell_grids) and sum([o['side']=='sell' for o in sell_orders]) * GRID_SIZE_PERCENT / 100 < MAX_INVESTED:
				qty = math.floor(MAX_INVESTED / sell_grids[i])
				sell_orders.append(place_order('sell', qty, sell_grids[i])['id'])
				
	# Function for cancelling all open orders
	def cancel_all_orders():
		open_orders = requests.get(f'{ENDPOINT}/v2/orders', headers=headers).json()
		for o in open_orders:
			cancel_order(o['id'])
			
	# Function for updating profit and loss
	def update_pl():
		global total_profit, pl_history, time_history
		open_orders = requests.get(f'{ENDPOINT}/v2/orders', headers=headers).json()
		total_pl = 0
		for o in open_orders:
			if o['side'] == 'buy':
				pl = (current_price - float(o['limit_price'])) * float(o['filled_qty'])
			else:
				pl = (float(o['limit_price']) - current_price) * float(o['filled_qty'])
			total_pl += pl
		total_profit = total_pl
		pl_history.append(total_profit)
		time_history.append(time.time())
		
	# Function for plotting price and profit/loss
	def plot_data():
		global current_price, pl_history, time_history
		plt.clf()
		plt.plot(time_history, pl_history, label='Profit/Loss')
		plt.plot(time_history[-1], current_price, 'bo', label='Current Price')
		plt.xlabel('Time')
		plt.ylabel('USD')
		plt.title('BTCUSD Trading Bot')
		plt.legend()
		plt.show()
		
	# Main trading loop
	while True:
		# Get current price
		r = requests.get(f'{ENDPOINT}/v2/assets/{SYMBOL}', headers=headers).json()
		current_price = float(r['last_price'])
		
		# Compute buy and sell grids
		compute_grids()
		
		# Cancel all open orders and place new orders
		cancel_all_orders()
		place_orders()
		
		# Update profit and loss and plot data
		update_pl()
		plot_data()
		
		# Wait before repeating loop
		time.sleep(PLOT_DELAY)
		
#########################################################

def gridbot3():
	# Set up API credentials
	load_dotenv()
	API_KEY = os.getenv('paper_api')
	SECRET_KEY = os.getenv('paper_secret')
	ENDPOINT = 'https://paper-api.alpaca.markets'
	
	# Set up trading parameters
	SYMBOL = 'BTCUSD'
	GRID_SIZE_PERCENT = 2 # Grid size as a percentage of current price
	NUM_GRIDS = 10 # Number of buy and sell grids on each side of current price
	MAX_INVESTED = 1000 # Maximum amount to invest in USD
	BUY_SELL_DELAY = 10 # Time in seconds between placing buy and sell orders
	PLOT_DELAY = 2 # Time in seconds between refreshing plot
	
	# Set up Alpaca API headers
	headers = {
	    'APCA-API-KEY-ID': API_KEY,
	    'APCA-API-SECRET-KEY': SECRET_KEY
	}
	
	# Initialize global variables
	current_price = None
	buy_grids = []
	sell_grids = []
	buy_orders = []
	sell_orders = []
	order_status = {}
	total_profit = 0
	pl_history = [0]
	time_history = [time.time()]
	
	# Functions for placing and cancelling orders
	def place_order(side, qty, price):
		data = {
		'symbol': SYMBOL,
		'qty': qty,
		'side': side,
		'type': 'limit',
		'time_in_force': 'gtc',
		'limit_price': price
		}
		r = requests.post(f'{ENDPOINT}/v2/orders', json=data, headers=headers)
		return r.json()
		
	def cancel_order(order_id):
		r = requests.delete(f'{ENDPOINT}/v2/orders/{order_id}', headers=headers)
		return r.json()
		
	# Function for computing grid prices
	def compute_grids():
		global current_price, buy_grids, sell_grids
		if current_price is None:
			return
		grid_size = current_price * GRID_SIZE_PERCENT / 100
		buy_grids = [current_price - (i+1) * grid_size for i in range(NUM_GRIDS)]
		sell_grids = [current_price + (i+1) * grid_size for i in range(NUM_GRIDS)]
		
	# Function for placing buy and sell orders
	def place_orders():
		global buy_orders, sell_orders
		buy_orders = []
		sell_orders = []
		for i in range(NUM_GRIDS):
			if i < len(buy_grids) and sum([o['side']=='buy' for o in buy_orders]) * GRID_SIZE_PERCENT / 100 < MAX_INVESTED:
				qty = math.floor(MAX_INVESTED / buy_grids[i])
				if i in order_status:
					if order_status[i]['side'] == 'buy' and order_status[i]['price'] != buy_grids[i]:
						cancel_order(order_status[i]['id'])
						order_status.pop(i)
					elif order_status[i]['side'] == 'sell':
						cancel_order(order_status[i]['id'])
						order_status.pop(i)
				if i not in order_status:
					order = place_order('buy', qty, buy_grids[i])
					buy_orders.append(order['id'])
					order_status[i] = {'id': order['id'], 'side': 'buy', 'price': buy_grids[i]}
			if i < len(sell_grids) and sum([o['side']=='sell' for o in sell_orders]) * GRID_SIZE_PERCENT / 100 < MAX_INVESTED:
				qty = math.floor(MAX_INVESTED / sell_grids[i])
				if i in order_status:
					if order_status[i]['side'] == 'sell' and order_status[i]['price'] != sell_grids[i]:
						cancel_order(order_status[i]['id'])
						order_status.pop(i)
					elif order_status[i]['side'] == 'buy':
						cancel_order(order_status[i]['id'])
						order_status.pop(i)
				if i not in order_status:
					order = place_order('sell', qty, sell_grids[i])
					sell_orders.append(order['id'])
					order_status[i] = {'id': order['id'], 'side': 'sell', 'price': sell_grids[i]}
					
	# Function for updating profit and loss
	def update_pl():
		global total_profit, pl_history, time_history
		open_orders = requests.get(f'{ENDPOINT}/v2/orders', headers=headers).json()
		total_pl = 0
		for o in open_orders:
			if o['id'] in order_status.values():
				i = list(order_status.keys())[list(order_status.values()).index(o['id'])]
				if o['side'] == 'buy':
					pl = (current_price - float(o['limit_price'])) * float(o['filled_qty'])
				else:
					pl = (float(o['limit_price']) - current_price) * float(o['filled_qty'])
				total_pl += pl
				order_status[i]['price'] = float(o['limit_price'])
		total_profit = total_pl
		pl_history.append(total_profit)
		time_history.append(time.time())
		
	# Function for plotting price and profit/loss
	def plot_data():
		global current_price, pl_history, time_history
		plt.clf()
		plt.plot(time_history, pl_history, label='Profit/Loss')
		plt.plot(time_history[-1], current_price, 'bo', label='Current Price')
		plt.xlabel('Time')
		plt.ylabel('USD')
		plt.title('BTCUSD Trading Bot')
		plt.legend()
		plt.show()
		
	# Main trading loop
	while True:
		# Get current price
		r = requests.get(f'{ENDPOINT}/v2/assets/{SYMBOL}/quote', headers=headers)
		current_price = float(r.json()['last_price'])
		
		# Compute buy and sell grids
		compute_grids()
		
		# Place buy and sell orders
		place_orders()
		
		# Update profit and loss
		update_pl()
		
		# Plot price and profit/loss
		plot_data()
		
		# Wait for next iteration
		time.sleep(PLOT_DELAY)
