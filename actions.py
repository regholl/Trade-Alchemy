import paperutils as pa
import liveutils as lv
from methods import methods

'''
this file will hold all the custom built routines I use for portfolio rebalancing, dollar cost averaging and trade scaling
'''

#							PAPER ACCOUNT
#########################################################

def paper_place_and_check_order(order):
	placed = pa.post_pa_order(order)
	order_id = placed['id']
	status = pa.get_pa_order_by_id(order_id)
	spent = status['notional']
	qty = status['filled_qty'] 
	symbol = status['symbol'] 
	price = status['filled_avg_price']
	result = status['status']
	message = f'{result}: You spent ${spent} to buy {qty} {symbol} at an average price of {price}'
	return message
	
	
#							LIVE ACCOUNT	
#########################################################


#							DATA REQUESTS 	
#########################################################
