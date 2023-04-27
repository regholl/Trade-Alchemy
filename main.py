from models import account, crypto, data, equity, orders, plot, storage
import routines as r
import assets
import json

type = 'paper'
data = account.get_watchlist(type)
print(data)
