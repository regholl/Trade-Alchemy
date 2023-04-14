from methods import methods
import requests
import json

url = methods.urls['data']
headers = methods.live_headers


#							STOCK DATA
#########################################################
def get_stock_snapshot(symbol):
	endpoint = f'/v2/stocks/{symbol}/snapshot'
	response = requests.get(url + endpoint, headers=headers)
	if response.status_code == 200:
		data = json.loads(response.content)
		return data
	else:
		print(f'Error retrieving snapshot for {symbol}. Status code: {response.status_code}')


def get_stock_spread(symbol):
	snapshot = get_stock_snapshot(symbol)
	latest_quote = snapshot['latestQuote']
	ask = latest_quote['ap']
	bid = latest_quote['bp']
	spread = {'ask': ask, 'bid':bid}
	return spread


