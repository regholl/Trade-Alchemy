import paperutils as pa
import liveutils as lv

order = {
	"symbol": "BTC/USD",
	"notional": "10.00",
	"side": "buy",
	"type": "market",
	"time_in_force": "gtc"
}

placed = pa.post_pa_order(order)
order_id = placed['id']
status = pa.get_pa_order_by_id(order_id)
spent = status['notional']
qty = status['filled_qty'] 
symbol = status['symbol'] 
price = status['filled_avg_price']

print(f'you spent ${spent} to buy {qty} {symbol} at an average price of {price}')
