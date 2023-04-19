import models.paper as pa
import models.data as dt
import models.live as lv
import models.storage as st

'''
this file will hold all the custom built routines I use for portfolio rebalancing, dollar cost averaging and trade scaling
'''

#                                                       PAPER ACCOUNT
#########################################################

def paper_dca():
	# Paper accoount dollar cost average. This routine checks all positions for negative PNL and buys the specified amout of each asset.
	# Gather account and position informatikn
	account_info = pa.get_account()
	portfolio_value = float(account_info['portfolio_value'])
	positions = pa.get_positions()
	# Create list of assets with higher average buy price than current price
	underwater_assets = []
	for position in positions:
		asset_symbol = position['symbol']
		avg_entry_price = float(position['avg_entry_price'])
		current_price = float(position['current_price'])
		if avg_entry_price > current_price:
			underwater_assets.append(asset_symbol)
	# Return list of assets with higher average buy price than current price
	if len(underwater_assets) > 0:
		print("The following assets in your portfolio have a higher average buy price than current price:")
		return underwater_assets
	else:
		print("All assets in your portfolio have a lower or equal average buy price than current price.")
		
		
#                                                       LIVE ACCOUNT
#########################################################



#                                                       DATA REQUESTS
#########################################################

