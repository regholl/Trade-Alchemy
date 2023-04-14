import paperutils as pa
import liveutils as lv
import actions as act

order = {
	"symbol": "BTC/USD",
	"notional": "10.00",
	"side": "buy",
	"type": "market",
	"time_in_force": "gtc"
}

place = act.paper_place_and_check_order(order)
print(place)
