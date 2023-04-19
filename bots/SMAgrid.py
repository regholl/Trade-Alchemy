from dotenv import load_dotenv
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

def smagrid():
	# Set up Alpaca API credentials
	load_dotenv()
	api_key = os.getenv('paper_api')
	api_secret = os.getenv('paper_secret')
	base_url = 'https://paper-api.alpaca.markets'
	
	# Define the grid parameters
	num_levels = 5
	grid_size = 0.01
	
	# Define the number of timesteps
	n_steps = 60
	
	# Define the interval between trades (in seconds)
	trade_interval = 60
	
	# Set up the plot
	plt.ion()
	fig, ax = plt.subplots()
	
	# Initialize the trade history
	trade_history = []
	
	# Define the function to get historical price data
	def get_price_data():
		response = requests.get(base_url + '/v2/assets/BTCUSD/candles', params={
		'limit': 1000,
		'timeframe': '1D'
		}, headers={'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret})
		data = response.json()
		prices = []
		for candle in data:
			prices.append(candle['close'])
		prices = np.array(prices).reshape(-1, 1)
		return prices
		
	# Define the function to get the current position
	def get_position():
		response = requests.get(base_url + '/v2/positions/BTCUSD', headers={'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret})
		position = response.json()
		return position
		
	# Define the function to execute a trade
	def execute_trade(side, price):
		response = requests.post(base_url + '/v2/orders', json={
		'symbol': 'BTCUSD',
		'qty': 1,
		'side': side,
		'type': 'limit',
		'time_in_force': 'gtc',
		'limit_price': price
		}, headers={'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret})
		order = response.json()
		return order
		
	# Define the function to close the position
	def close_position():
		response = requests.delete(base_url + '/v2/positions/BTCUSD', headers={'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret})
		return response
		
	# Define the function to update the plot
	def update_plot(x, y, trades):
		ax.clear()
		ax.plot(x, y, label='Price')
		for trade in trades:
			if trade['side'] == 'buy':
				ax.scatter(trade['timestamp'], trade['price'], color='green', marker='^', label='Buy')
			elif trade['side'] == 'sell':
				ax.scatter(trade['timestamp'], trade['price'], color='red', marker='v', label='Sell')
		ax.legend()
		plt.draw()
		plt.pause(0.001)
		
	# Get the historical price data
	prices = get_price_data()
	
	# Define the function to calculate the SMA
	def calculate_sma(prices, n):
		sma = np.zeros_like(prices)
		for i in range(n-1, len(prices)):
			sma[i] = np.mean(prices[i-n+1:i+1])
		return sma
		
	# Initialize the model
	sma_window = 10
	sma = calculate_sma(prices, sma_window)
	
	# Define the grid
	grid = []
	for i in range(num_levels):
		grid.append(prices[-1][0] * (1 - grid_size) ** (num_levels - i - 1))
		
	# Start trading
	while True:
		try:
			current_position = get_position()
			
			if current_position['side'] == 'none':
				if prices[-1][0] >= sma[-1] and prices[-2][0] < sma[-2]:
					for price in grid:
						if price <= prices[-1][0]:
							execute_trade('buy', price)
							trade_history.append({'side': 'buy', 'price': price, 'timestamp': time.time()})
							grid.remove(price)
							update_plot(range(len(prices)), prices, trade_history)
							break
				elif prices[-1][0] <= sma[-1] and prices[-2][0] > sma[-2]:
					for price in reversed(grid):
						if price >= prices[-1][0]:
							execute_trade('sell', price)
							trade_history.append({'side': 'sell', 'price': price, 'timestamp': time.time()})
							grid.remove(price)
							update_plot(range(len(prices)), prices, trade_history)
							break
							
			elif current_position['side'] == 'long':
				if prices[-1][0] >= sma[-1]:
					execute_trade('sell', prices[-1][0])
					trade_history.append({'side': 'sell', 'price': prices[-1][0], 'timestamp': time.time()})
					update_plot(range(len(prices)), prices, trade_history)
					
			elif current_position['side'] == 'short':
				if prices[-1][0] <= sma[-1]:
					execute_trade('buy', prices[-1][0])
					trade_history.append({'side': 'buy', 'price': prices[-1][0], 'timestamp': time.time()})
					update_plot(range(len(prices)), prices, trade_history)
					
			prices = np.vstack((prices, get_price_data()))
			sma = np.append(sma, calculate_sma(prices, sma_window)[-1])
			time.sleep(trade_interval)
			
		except Exception as e:
			print(e)
			time.sleep(trade_interval)
			
'''
In this revised code, we use a simple moving average (SMA) to predict the future price of BTC. The `calculate_sma()` function calculates the SMA based on the historical price data, and the `sma` array is used to track the moving average over time. We simply compare the current price to the current SMA to decide whether to buy or sell.
'''

