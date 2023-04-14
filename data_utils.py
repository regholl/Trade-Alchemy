import methods
import requests
import json

s_url = methods.urls['s_data']
c_url = methods.urls['c_data']
headers = methods.live_headers


#							STOCK DATA
#########################################################
def get_stock_snapshot(symbol):
	# Returns most recent details of the symbol passed in
	endpoint = f'/v2/stocks/{symbol}/snapshot'
	response = requests.get(s_url + endpoint, headers=headers)
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



#							CRYPTO DATA
#########################################################

def get_xbbo(symbol):
	# Returns cross exchange best bid for symbol passed in
	endpoint = f'/v1beta1/crypto/{symbol}/xbbo/latest'
	response = requests.get(c_url + endpoint, headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving XBBO for {symbol}. Status code: {response.status_code}')
		

def get_crypto_spread(symbol):
	# Returns bid and ask for symbol passed in
	quote = get_xbbo(symbol)
	cross = quote['xbbo']
	ax = cross['ax']
	ask = cross['ap']
	bid = cross['bp']
	spread = {'ask':ask, 'bid':bid, 'exchange':ax}
	return spread
	
