import models as m

def run_dca_buys(qty):
	pos = m.paper.get_negative_pnl()
	for i in pos:
		order = m.paper.build_dca_order(i, qty)
		m.paper.post_order(order) 
		
