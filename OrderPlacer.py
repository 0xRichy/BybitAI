import ccxt
import logging

class OrderPlacer:
    def __init__(self, exchange):
        self.exchange = exchange

    def place_market_order(self, symbol, side, quantity, leverage):
        for _ in range(3):  # retry 3 times
            try:
                order = self.exchange.create_market_order(symbol, side, quantity, {'leverage': leverage})
                trade_price = order['price']
                trade_quantity = order['amount']
                trade_side = order['side']
                trade_type = order['type']
                logging.info(f"Trade Details: Price: {trade_price}, Quantity: {trade_quantity}, Side: {trade_side}, Type: {trade_type} at {time.time()}")
                return order
            except ccxt.NetworkError as e:
                logging.error(f"Network error while placing order: {e}")
                continue
            break

    def get_account_balance(self):
        for _ in range(3):  # retry 3 times
            try:
                balance = self.exchange.fetch_balance()
                logging.info(f"Account balance fetched: {balance['USDT']['free']} at {time.time()}")
                return balance['USDT']['free']
            except ccxt.NetworkError as e:
                logging.error(f"Network error while fetching account balance: {e}")
                continue
            break
