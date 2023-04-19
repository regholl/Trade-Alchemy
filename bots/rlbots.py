from dotenv import load_dotenv
import requests
import numpy as np
import time
import os

def rlbot1():
	# Set up Alpaca API credentials
	load_dotenv()
	api_key = os.getenv('paper_api')
	api_secret = os.getenv('paper_secret')
	base_url = 'https://paper-api.alpaca.markets'
	
	# Define the reinforcement learning agent
	class RLAgent:
		def __init__(self, state_size, action_size):
			self.state_size = state_size
			self.action_size = action_size
			self.q_table = np.zeros((self.state_size, self.action_size))
			
		def act(self, state):
			action = np.argmax(self.q_table[state, :])
			return action
			
		def learn(self, state, action, reward, next_state, done):
			if done:
				target = reward
			else:
				target = reward + np.max(self.q_table[next_state, :])
			self.q_table[state, action] += 0.1 * (target - self.q_table[state, action])
			
	# Define constants
	EPISODES = 100
	MAX_TRADES = 100
	INITIAL_BALANCE = 10000
	COMMISSION = 0.01
	
	# Define states and actions
	states = [0, 1, 2]  # 0 = short, 1 = neutral, 2 = long
	actions = [0, 1]  # 0 = sell, 1 = buy
	
	# Create the RL agent
	agent = RLAgent(len(states), len(actions))
	
	# Run the reinforcement learning algorithm
	while True:
		# Reset the environment
		balance = INITIAL_BALANCE
		position = 0
		trades = 0
		done = False
		
		# Loop until the episode is done
		while not done:
			# Get the current state
			if position > 0:
				state = states[2]
			elif position < 0:
				state = states[0]
			else:
				state = states[1]
				
			# Choose an action
			action = agent.act(state)
			
			# Execute the action
			if action == 0:  # sell
				if position < 0:
					response = requests.post(base_url + '/v2/orders', json={
					'symbol': 'BTCUSD',
					'qty': abs(position),
					'side': 'buy',
					'type': 'market',
					'time_in_force': 'gtc'
					}, headers={'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret})
					balance += (1 - COMMISSION) * abs(position) * response.json()['filled_avg_price']
					position = 0
					trades += 1
				else:
					response = requests.post(base_url + '/v2/orders', json={
					'symbol': 'BTCUSD',
					'qty': 1,
					'side': 'sell',
					'type': 'market',
					'time_in_force': 'gtc'
					}, headers={'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret})
					position -= 1
			elif action == 1:  # buy
				if position > 0:
					response = requests.post(base_url + '/v2/orders', json={
					'symbol': 'BTCUSD',
					'qty': abs(position),
					'side': 'sell',
					'type': 'market',
					'time_in_force': 'gtc'
					}, headers={'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret})
					balance -= (1 + COMMISSION) * abs(position) * response.json()['filled_avg_price']
					position = 0
					trades += 1
				else:
					response = requests.post(base_url + '/v2/orders', json={
					'symbol': 'BTCUSD',
					'qty': 1,
					'side': 'buy',
					'type': 'market',
					'time_in_force': 'gtc'
					}, headers={'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret})
					position += 1
					
			# Get the reward and the next state
			response = requests.get(base_url + '/v2/assets/BTCUSD', headers={'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret})
			price = float(response.json()['bid_price'])
			if position > 0:
				reward = price - entry_price
			elif position < 0:
				reward = entry_price - price
			else:
				reward = 0
			next_state = states[1] if trades >= MAX_TRADES else (states[2] if position > 0 else states[0])
			
			# Learn from the experience
			agent.learn(state, action, reward, next_state, done)
			
			# Check if the episode is done
			if trades == MAX_TRADES:
				done = True
				
			# Wait for 10 seconds before executing the next action
			time.sleep(10)

