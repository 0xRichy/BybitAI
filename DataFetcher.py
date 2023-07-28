import ccxt
import logging
import os
from dotenv import load_dotenv

load_dotenv()

class DataFetcher:
    def __init__(self, exchange):
        self.exchange = exchange

    def fetch_real_time_data(self, symbol, timeframe):
        for _ in range(3):  # retry 3 times
            try:
                ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=1)
                logging.info(f"Successfully fetched data for {symbol} at {time.time()}")
                return np.array([candle[4] for candle in ohlcv])
            except ccxt.NetworkError as e:
                logging.error(f"Network error while fetching data: {e}")
                continue
            break
