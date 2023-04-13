from methods import methods
import requests
import json
'''This file pulls the urls, endpoints and headers from the methods file and structures all calls to the alpaca paper api'''

url = methods.urls['paper']
endpoint = methods.endpoints
headers = methods.paper_headers


def get_pa_account():
	# Returns a dictionary containing paper account details
	response = requests.get(url + endpoint['account'], headers=headers)
	account = response.json()
	return account


def get_pa_positions():
	# Returns a list of all open positions
	reaponse = requests.get(urls + endpoint['positions'], headers=headers)
	positions = reaponse.json()
	return positions


def get_pa_orders():
	# Returns a list of ALL open orders
	response = requests.get(url + endpoint['orders'], headers=headers)
	orders = response.json()
	return orders


def get_pa_order_by_id(id):
	response = requests.get(url + endpoint['orders'] + f"/{id}", headers=headers)
	details = response.json()
	return details
	
	
def post_pa_order(order):
	''' takes a json object formatted as a string dictionary, fractional and notional only work as "market" and "day" orders
	
		symbol - ticker name or currency pair
		qty - quantity of shares (cant be used with notional)
		notional - dollar amount (cant be used with qty)
		side - buy or sell
		type - market, limit, stop, stop_limit, trailing_stop
		time_in_force - day, gtc, opg, cls, ioc, fok
		stop_price (optional)
		trail_price (optional)
		trail_percent (optional)
		extended_hours (optional - boolean)
		client_order_id (optional)
		order_class (optional) simple, bracket, oto, oco
		take_profit (optional)
		stop_loss (optional)
		
		crypro orders only support GTC or IOC types
		'''
	response = requests.post(url + endpoint['orders'], headers=headers, json=order)
	return response.json()
