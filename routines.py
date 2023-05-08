from models import account, crypto, data, equity, orders, positions, plot, storage


def get_losing_crypto(type):
	# Returns a list of cryptos that are cheaper now than the average buy price
	crypto = []
	losers = []
	list = account.get_all_positions(type)
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
	list = account.get_all_positions(type)
	for i in list:
		if i['asset_class'] == 'us_equity':
			equities.append(i)
	for i in equities:
		if i['avg_entry_price'] > i['current_price']:
			losers.append(i['symbol'])
	return losers


def dca_order(type):
	pass


def scale_in(type):
	pass
