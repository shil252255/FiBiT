from config import binance_api_key, binance_api_secret
from binance.client import Client
import time
from pprint import pprint
import dotenv


class Binance:
    def __init__(self, public_key = '', secret_key = '', sync = False):
        self.time_offset = 0
        self.b = Client(public_key, secret_key)
        if sync:
            self.time_offset = self._get_time_offset()

    def _get_time_offset(self):
        res = self.b.get_server_time()
        return res['serverTime'] - (int(time.time() * 1000))

    def synced(self, fn_name, **args):
        args['timestamp'] = int(time.time() * 1000 + self.time_offset)
        return getattr(self.b, fn_name)(**args)

client = Client(binance_api_key, binance_api_secret)
binance = Binance(binance_api_key, binance_api_secret, True)
a=binance.synced('get_account',)
my_coins = {}
for b in a['balances']:
    if float(b['free'])>0:
        my_coins[b['asset']] = float(b['free'])
pprint(my_coins)

all_symbols = list(price['symbol'] for price in client.get_all_tickers())
for coin in my_coins:
    for symbol in all_symbols:
        if coin in symbol[:-4] and 'USDT' in symbol:
            print(symbol)
#pprint(all_symbols)
# print(client.get_account(timestamp=binance.time_offset/1000))

'''from binance.enums import *
order = client.create_order(
    symbol='BUSDUSDT',
    side=SIDE_SELL,
    type=ORDER_TYPE_MARKET,
    # timeInForce=TIME_IN_FORCE_GTC,
    quantity=11,
    # price='0.00001'
    timestamp=int(time.time() * 1000 + binance.time_offset)
    )'''