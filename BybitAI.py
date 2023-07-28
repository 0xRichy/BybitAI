import ccxt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import time
import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace these with your Bybit API credentials
bybit_api_key = 'YOUR_API_KEY'
bybit_secret_key = 'YOUR_SECRET_KEY'

# Replace this with your Telegram Bot API token and chat_id
telegram_token = 'YOUR_TELEGRAM_BOT_TOKEN'
telegram_chat_id = 'YOUR_TELEGRAM_CHAT_ID'

# Initialize the Bybit API client for derivatives trading
bybit_exchange = ccxt.bybit({'apiKey': bybit_api_key, 'secret': bybit_secret_key, 'options': {'defaultType': 'future'}})

# Initialize the Telegram Bot
telegram_bot = Bot(token=telegram_token)

# Set up logging to Telegram
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.StreamHandler(telegram_bot.send_message))

class DataFetcher:
    def __init__(self, exchange):
        self.exchange = exchange

    def fetch_real_time_data(self, symbol, timeframe):
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=1)
            return np.array([candle[4] for candle in ohlcv])
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return None

class IndicatorGenerator:
    def generate_ai_indicator(self, data):
        ema_period = 12
        ema = np.mean(data[-ema_period:])
        return ema

class MachineLearningModel:
    def __init__(self):
        self.classifier = RandomForestClassifier()

    def create_dataset(self, data, window_size):
        X, y = [], []
        for i in range(len(data) - window_size - 1):
            window = data[i:i+window_size]
            X.append(window)
            y.append(1 if data[i+window_size] > self.generate_ai_indicator(window) else -1)
        return np.array(X), np.array(y)

    def train(self, X, y):
        self.classifier.fit(X, y)

    def predict(self, data):
        return self.classifier.predict([data])[0]

class OrderPlacer:
    def __init__(self, exchange):
        self.exchange = exchange

    def place_market_order(self, symbol, side, quantity, leverage):
        try:
            order = self.exchange.create_market_order(symbol, side, quantity, {'leverage': leverage})

            # Log trade details
            trade_price = order['price']
            trade_quantity = order['amount']
            trade_side = order['side']
            trade_type = order['type']
            logger.info(f"Trade Details: Price: {trade_price}, Quantity: {trade_quantity}, Side: {trade_side}, Type: {trade_type}")

            return order
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None

    def get_account_balance(self):
        try:
            balance = self.exchange.fetch_balance()
            return balance['USDT']['free']
        except Exception as e:
            logger.error(f"Error fetching account balance: {e}")
            return 0.0

def main():
    # Fetch real-time data for a specific trading pair and timeframe
    symbol = 'BTC/USDT'  # Use the perpetual BTC/USDT contract
    timeframe = '1m'  # Use a lower timeframe for real-time streaming, '1m' is just an example
    window_size = 10

    # Define the leverage for your trades
    leverage = 50  # Replace with your desired leverage

    # Define the desired risk percentage (e.g., 2%)
    risk_percentage = 2

    data_fetcher = DataFetcher(bybit_exchange)
    indicator_generator = IndicatorGenerator()
    ml_model = MachineLearningModel()
    order_placer = OrderPlacer(bybit_exchange)

    # Main trading loop
    while True:
        try:
            # Fetch real-time data
            real_time_data = data_fetcher.fetch_real_time_data(symbol, timeframe)

            if real_time_data is not None:
                # Generate AI indicator on real-time data
                ai_indicator = indicator_generator.generate_ai_indicator(real_time_data)

                # Create machine learning dataset
                X, y = ml_model.create_dataset(real_time_data, window_size)

                # Train the classifier
                ml_model.train(X, y)

                # Make prediction for the next data point
                next_data_point = real_time_data[-window_size:]
                prediction = ml_model.predict(next_data_point)

                # Define trading signal based on the prediction
                signal = 'BUY' if prediction == 1 else 'SELL'

                # Get account balance in USDT
                account_balance = order_placer.get_account_balance()

                # Calculate the trade amount in USDT based on available balance and risk percentage
                risk_amount = (account_balance * risk_percentage) / 100
                trade_amount = min(risk_amount, account_balance)  # Limit trade amount to available balance

                # Log trading signal and trade amount
                logger.info(f"Signal: {signal}, Trade Amount (USDT): {trade_amount:.2f}")

                # Execute the trade
                if signal == 'BUY':
                    order_placer.place_market_order(symbol, 'buy', trade_amount, leverage)
                elif signal == 'SELL':
                    order_placer.place_market_order(symbol, 'sell', trade_amount, leverage)

            # Add a sleep interval to control the trading frequency (e.g., sleep for 1 minute)
            time.sleep(60)

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
