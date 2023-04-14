import methods
import requests
import json

'''This file pulls the urls, endpoints and headers from the methods file and structures all calls to the alpaca paper api'''

url = methods.urls['paper']
endpoint = methods.endpoints
headers = methods.paper_headers


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
	response = requests.post(url + endpoint['orders'], headers=headers, json=order)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error placing order. Status code: {response.status_code}')
