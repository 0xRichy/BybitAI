from DataFetcher import DataFetcher
from IndicatorGenerator import IndicatorGenerator
from MachineLearningModel import MachineLearningModel
from OrderPlacer import OrderPlacer
import ccxt
import os
from dotenv import load_dotenv
import time
import logging
from telegram import Bot

load_dotenv()

# Get Bybit API credentials from environment variables
bybit_api_key = os.getenv('BYBIT_API_KEY')
bybit_secret_key = os.getenv('BYBIT_SECRET_KEY')

# Get Telegram Bot API token and chat_id from environment variables
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

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

                # Implement dynamic risk management: risk more when confident about a trade and less when not
                confidence = abs(prediction - 0.5) * 2  # Convert prediction to a confidence score between 0 and 1
                trade_amount = min(confidence * risk_amount, account_balance)  # Limit trade amount to available balance

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
