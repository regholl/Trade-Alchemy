from dotenv import load_dotenv
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

def historicalgrid():
	# Set up API credentials
	load_dotenv()
	api_key = os.getenv('paper_api')
	secret_key = os.getenv('paper_secret')
	base_url = 'https://paper-api.alpaca.markets'
	headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': secret_key}
	
	# Set investment size
	investment = 1000
	
	# Collect historical data for BTCUSD
	symbol = 'BTCUSD'
	timeframe = '1D'
	limit = 1000
	url = f'{base_url}/v2/assets/{symbol}/history?period={timeframe}&limit={limit}'
	response = requests.get(url, headers=headers)
	if response.status_code != 200:
		print(f'Error getting historical data for {symbol}. Status code: {response.status_code}')
		exit()
	data = response.json()
	df = pd.DataFrame(data['candles'])
	df.set_index('time', inplace=True)
	df.index = pd.to_datetime(df.index, unit='s')
	
	# Calculate the initial grid levels
	num_levels = 5
	grid_levels = []
	for i in range(num_levels + 1):
		level = df['low'].min() + (i * (df['high'].max() - df['low'].min())) / num_levels
		grid_levels.append(level)
		
	# Implement the trading strategy
	while True:
		# Get the current balance and portfolio value
		url = f'{base_url}/v2/accounts/balances'
		response = requests.get(url, headers=headers)
		if response.status_code != 200:
			print(f'Error getting account balances. Status code: {response.status_code}')
			time.sleep(60)
			continue
		balances = response.json()
		account_balance = float(balances['equity'])
		portfolio_value = float(balances['portfolio_value'])
		
		# Ensure investment never exceeds allotted amount
		num_buys = investment // 0.001
		num_sells = num_buys
		
		# Get the current open orders
		url = f'{base_url}/v2/orders?status=open&symbol={symbol}'
		response = requests.get(url, headers=headers)
		if response.status_code != 200:
			print(f'Error getting open orders for {symbol}. Status code: {response.status_code}')
			time.sleep(60)
			continue
		open_orders = response.json()
		
		# Match open buy and sell orders
		buy_orders = []
		sell_orders = []
		for order in open_orders:
			if order['side'] == 'buy':
				buy_orders.append(order)
			elif order['side'] == 'sell':
				sell_orders.append(order)
		for buy_order in buy_orders:
			for sell_order in sell_orders:
				if sell_order['created_at'] > buy_order['created_at'] and sell_order['filled_at'] is not None:
					pnl = float(sell_order['filled_qty']) * (float(sell_order['filled_avg_price']) - float(buy_order['filled_avg_price']))
					print(f'Filled Buy Order: {buy_order["id"]}, Filled Sell Order: {sell_order["id"]}, Profit/Loss: {pnl:.2f}')
					
		# Adjust the grid levels based on the last executed order
		if len(buy_orders) > len(sell_orders):
			last_order = buy_orders[-1]
			last_price = float(last_order['filled_avg_price'])
			grid_levels = [level * (1 - 0.01) for level in grid_levels if level < last_price] + [level * (1 + 0.01) for level in grid_levels if level >= last_price]
		elif len(sell_orders) > len(buy_orders):
			last_order = sell_orders[-1]
			last_price = float(last_order['filled_avg_price'])
			grid_levels = [level * (1 - 0.01) for level in grid_levels if level <= last_price] + [level * (1 + 0.01) for level in grid_levels if level > last_price]
			
		# Place new buy and sell orders based on the updated grid levels
		for level in grid_levels:
			# Place buy order at level - 1%
			buy_price = level * 0.99
			data = {'symbol': symbol, 'qty': f'0.001', 'side': 'buy', 'type': 'limit', 'time_in_force': 'gtc', 'limit_price': str(buy_price)}
			url = f'{base_url}/v2/orders'
			response = requests.post(url, headers=headers, json=data)
			if response.status_code == 201:
				buy_order = response.json()
				buy_orders.append(buy_order)
			else:
				print(f'Error placing buy order at {buy_price}. Status code: {response.status_code}')
				
			# Place sell order at level + 1%
			sell_price = level * 1.01
			data = {'symbol': symbol, 'qty': f'0.001', 'side': 'sell', 'type': 'limit', 'time_in_force': 'gtc', 'limit_price': str(sell_price)}
			response = requests.post(url, headers=headers, json=data)
			if response.status_code == 201:
				sell_order = response.json()
				sell_orders.append(sell_order)
			else:
				print(f'Error placing sell order at {sell_price}. Status code: {response.status_code}')
				
		# Plot the price of BTC, the grid levels, and the orders
		plt.plot(df['close'])
		for level in grid_levels:
			plt.axhline(y=level, color='gray', linestyle='--')
		for order in buy_orders:
			plt.plot(pd.to_datetime(order['created_at']), order['limit_price'], 'go')
		for order in sell_orders:
			plt.plot(pd.to_datetime(order['created_at']), order['limit_price'], 'ro')
		plt.title('BTCUSD Grid Trading')
		plt.legend(['Price', 'Grid Levels', 'Buy Orders', 'Sell Orders'])
		plt.show()
		plt.clf()
		
		# Wait for a minute before checking again
		time.sleep(60)
	
'''
This code implements a grid trading strategy for Bitcoin (BTC) against the US Dollar (USD). It does the following:
Gets historical data for BTCUSD from the Alpaca API to calculate initial grid levels.
Connects to an Alpaca account and gets the current balance and position value.
Ensures the amount invested never exceeds the allotted amount.
Gets any open orders for the BTCUSD symbol.
Matches open buy and sell orders to calculate profits or losses.
Adjusts the grid levels up or down based on the last executed order.
Places new buy and sell orders at the updated grid levels.
Plots the price of BTC, grid levels, and open orders to visualize the strategy.
Waits 60 seconds before repeating the strategy.
The goal of the strategy is to profit from the volatility of Bitcoin prices by buying when the price dips below a grid level and selling when the price rises above a grid level. The grid levels act as support and resistance levels to guide entry and exit points.
'''

