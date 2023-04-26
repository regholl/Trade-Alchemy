import models as m

def paper_dca(qty):
	pos = m.paper.get_negative_pnl()
	for i in pos:
		order = m.paper.build_notional_order(i, qty, 'buy')
		m.paper.post_order(order) 

def live_dca(qty):
	pos = m.live.get_negative_pnl()
	for i in pos:
		order = m.live.build_notional_order(i, qty, 'buy')
		m.live.post_order(order)
