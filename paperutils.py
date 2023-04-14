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
	return response.json()


def get_pa_positions():
	# Returns a list of all open positions
	reaponse = requests.get(urls + endpoint['positions'], headers=headers)
	return response.json()


def get_pa_orders():
	# Returns a list of ALL open orders
	response = requests.get(url + endpoint['orders'], headers=headers)
	return response.json()


def get_pa_order_by_id(id):
	# Returns details of the order id that is passed in
	response = requests.get(url + endpoint['orders'] + f"/{id}", headers=headers)
	return response.json()
	
	
def post_pa_order(order):
	# Accepts a dict object and returns order details
	response = requests.post(url + endpoint['orders'], headers=headers, json=order)
	return response.json()
