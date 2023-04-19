import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
from time import sleep
import os

def complexgrid():
	# Set up Alpaca API credentials
	load_dotenv()
	API_KEY = os.getenv('paper_api')
	SECRET_KEY = os.getenv('paper_secret')
	ENDPOINT_URL = 'https://paper-api.alpaca.markets'
	
	# Set up grid trading parameters
	investment_amount = 1000 # Set your investment amount
	grid_spacing = 0.05 # Set the grid spacing as a percentage of the current price
	max_orders = 10 # Set the maximum number of orders to maintain in the grid
	stop_loss = 0.02 # Set the stop loss as a percentage
	take_profit = 0.05 # Set the take profit as a percentage
	
	# Set up technical indicators
	def calculate_sma(data, period):
		return data['close'].rolling(window=period).mean()
		
	def calculate_bollinger_bands(data, period, num_std):
		rolling_mean = data['close'].rolling(window=period).mean()
		rolling_std = data['close'].rolling(window=period).std()
		upper_band = rolling_mean + (rolling_std * num_std)
		lower_band = rolling_mean - (rolling_std * num_std)
		return upper_band, lower_band
		
	def calculate_rsi(data, period):
		delta = data['close'].diff()
		gain = delta.where(delta > 0, 0)
		loss = -delta.where(delta < 0, 0)
		avg_gain = gain.rolling(window=period).mean()
		avg_loss = loss.rolling(window=period).mean()
		rs = avg_gain / avg_loss
		rsi = 100 - (100 / (1 + rs))
		return rsi
		
	# Set up function to place orders
	def place_order(symbol, qty, side, type, time_in_force, limit_price=None, stop_price=None):
		data = {
		'symbol': symbol,
		'qty': qty,
		'side': side,
		'type': type,
		'time_in_force': time_in_force
		}
		if limit_price is not None:
			data['limit_price'] = limit_price
		if stop_price is not None:
			data['stop_price'] = stop_price
		response = requests.post(
		f'{ENDPOINT_URL}/v2/orders',
		headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY},
		json=data
		)
		return json.loads(response.content)
		
	# Set up function to get account information
	def get_account():
		response = requests.get(
		f'{ENDPOINT_URL}/v2/account',
		headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
		)
		return json.loads(response.content)
		
	# Set up function to get historical data
	def get_historical_data(symbol, interval, period):
		params = {
		'symbol': symbol,
		'interval': interval,
		'limit': period
		}
		response = requests.get(
		f'{ENDPOINT_URL}/v2/stocks/{symbol}/candles',
		headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY},
		params=params
		)
		data = json.loads(response.content)
		df = pd.DataFrame(data)
		df['timestamp'] = pd.to_datetime(df['t'], unit='s')
		df.set_index('timestamp', inplace=True)
		return df
		
	# Set up function to place grid orders
	def place_grid_orders(current_price, investment_amount, grid_spacing, max_orders):
		orders = []
		for i in range(-max_orders, max_orders+1):
			price = current_price * (1 + i * grid_spacing)
			if price > current_price:
				side = 'buy'
				qty = (investment_amount / max_orders) / price
			else:
				side = 'sell'
				qty = (investment_amount / max_orders) / current_price
			orders.append({'price': price, 'side': side, 'qty': qty})
		return orders
		
	# Set up function to update grid orders
	def update_grid_orders(current_orders, new_orders):
		# Remove any old orders that are no longer needed
		for order in current_orders:
			if order['price'] not in [o['price'] for o in new_orders]:
				response = requests.delete(
				f'{ENDPOINT_URL}/v2/orders/{order["id"]}',
				headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
				)
		# Place any new orders that are needed
		for order in new_orders:
			if order['price'] not in [o['price'] for o in current_orders]:
				response = place_order('BTCUSD', order['qty'], order['side'], 'limit', 'gtc', order['price'])
				
	# Set up function to get current positions
	def get_positions():
		response = requests.get(
		f'{ENDPOINT_URL}/v2/positions',
		headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}
		)
		return json.loads(response.content)
		
	# Set up function to plot data
	def plot_data(df, current_orders, profit_loss):
		fig, ax = plt.subplots(figsize=(10,5))
		ax.plot(df['close'], color='blue', label='Price')
		for order in current_orders:
			if order['side'] == 'buy':
				ax.axvline(x=order['timestamp'], color='green', linestyle='--', label='Buy Order')
			else:
				ax.axvline(x=order['timestamp'], color='red', linestyle='--', label='Sell Order')
		ax.set_xlabel('Time')
		ax.set_ylabel('Price')
		ax2 = ax.twinx()
		ax2.plot(profit_loss, color='purple', label='Profit/Loss')
		ax2.set_ylabel('Profit/Loss')
		fig.legend()
		plt.show()
		
	# Main loop
	while True:
		# Get current price
		data = get_historical_data('BTCUSD', '1Min', 30)
		current_price = data['close'][-1]
		
		# Place grid orders
		orders = place_grid_orders(current_price, investment_amount, grid_spacing, max_orders)
		update_grid_orders(current_orders, orders)
		current_orders = orders
		
		# Check if stop loss or take profit conditions have been met
		positions = get_positions()
		for position in positions:
			if position['symbol'] == 'BTCUSD':
				if float(position['unrealized_pl']) < -stop_loss*investment_amount:
					response = place_order('BTCUSD', abs(float(position['qty'])), 'sell', 'market', 'gtc')
				elif float(position['unrealized_pl']) > take_profit*investment_amount:
					response = place_order('BTCUSD', abs(float(position['qty'])), 'sell', 'market', 'gtc')
					
		# Calculate technical indicators
		sma = calculate_sma(data, 20)
		upper_band, lower_band = calculate_bollinger_bands(data, 20, 2)
		rsi = calculate_rsi(data, 14)
		
		# Plot data
		profit_loss = [float(p['unrealized_pl']) for p in positions]
		plot_data(data, current_orders, profit_loss)
		
		# Wait for next iteration
		sleep(60)
		
		
'''
This code sets up a loop that runs indefinitely, periodically getting the current price of BTCUSD, placing a grid of buy and sell orders around the current price, and checking if any stop loss or take profit conditions have been met on the current positions. It also calculates some technical indicators (SMA, Bollinger Bands, and RSI) and plots the price data along with the current orders and profit/loss.
'''

