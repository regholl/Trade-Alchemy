from models import account, crypto, data, equity, orders, positions, plot, storage
import assets


def get_losing_crypto(type):
	# Returns a list of cryptos that are cheaper now than the average buy price
	crypto = []
	losers = []
	list = positions.get_all_positions(type)
	for i in list:
		if i['asset_class'] == 'crypto':
			crypto.append(i)
	for i in crypto:
		if i['avg_entry_price'] > i['current_price']:
			losers.append(i['symbol'])
	return losers
	
	
def get_losing_equities(type):
	# Returns a list of equities that are cheaper now than the average buy price
	equities = []
	losers = []
	list = positions.get_all_positions(type)
	for i in list:
		if i['asset_class'] == 'us_equity':
			equities.append(i)
	for i in equities:
		if i['avg_entry_price'] > i['current_price']:
			losers.append(i['symbol'])
	return losers
	
	
def batch_crypro_order(type, amount):
	# Places a batch or orders based on the assets list and amount provided
	cryptos = assets.crypto
	orders = crypto.crypto_buy_list(cryptos, amount, type)
	orders.post_list_of_orders(type, orders)
	

def crypto_dca_order(type, amount):
	data = get_losing_crypto(type)
	for i in data:
		order = {
			'symbol': i,
			'notional': amount,
			'type': 'market',
			'side': 'buy',
			'time_in_force': 'gtc'
		}
		orders.post_order(type, order)
		

def equity_dca_order(type, amount):
	data = get_losing_equities(type)
	for i in data:
		order = {
			'symbol': i,
			'notional': amount,
			'type': 'market',
			'side': 'buy',
			'time_in_force': 'gtc'
		}
		orders.post_order(type, order)


def scale_in(type):
	pass
