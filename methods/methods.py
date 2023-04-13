from dotenv import load_dotenv
import os
''' This files sets up an easy to reference list of all urls and endpoints as well as all the headers required for api calls.

live headers are required for most market data api calls
'''

urls = {
 'paper': 'https://paper-api.alpaca.markets',
 'live': 'https://api.alpaca.markets',
 'data': 'https://data.alpaca.markets'
}
endpoints = {'account': '/v2/account', 'orders': '/v2/orders', 'positions': '/v2/positions'}

load_dotenv()
paper_api = os.getenv("paper_api")
paper_secret = os.getenv("paper_secret")
live_api = os.getenv("live_api")
live_secret = os.getenv("live_secret")

paper_headers = {
 'Apca-Api-Key-Id': paper_api,
 'Apca-Api-Secret-Key': paper_secret
}

live_headers = {
 'Apca-Api-Key-Id': live_api,
 'Apca-Api-Secret-Key': live_secret
}
