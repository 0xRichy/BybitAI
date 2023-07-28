import ccxt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import time

# Replace these with your Bybit API credentials
bybit_api_key = 'YOUR_API_KEY'
bybit_secret_key = 'YOUR_SECRET_KEY'

# Initialize the Bybit API client for derivatives trading
bybit_exchange = ccxt.bybit({'apiKey': bybit_api_key, 'secret': bybit_secret_key, 'options': {'defaultType': 'future'}})

# Define function to fetch real-time market data
def fetch_real_time_data(symbol, timeframe):
    try:
        ohlcv = bybit_exchange.fetch_ohlcv(symbol, timeframe, limit=1)
        return np.array([candle[4] for candle in ohlcv])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

# Define function to generate AI indicator
def generate_ai_indicator(data):
    # Your AI indicator generation code goes here
    # For illustration, let's assume a simple moving average
    return np.mean(data)

# Define function to create machine learning dataset
def create_dataset(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size - 1):
        window = data[i:i+window_size]
        X.append(window)
        y.append(1 if data[i+window_size] > generate_ai_indicator(window) else -1)
    return np.array(X), np.array(y)

# Define function to place a market order
def place_market_order(symbol, side, quantity, leverage):
    try:
        order = bybit_exchange.create_market_order(symbol, side, quantity, {'leverage': leverage})
        return order
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

# Define function to get account balance in USDT
def get_account_balance():
    try:
        balance = bybit_exchange.fetch_balance()
        return balance['USDT']['free']
    except Exception as e:
        print(f"Error fetching account balance: {e}")
        return 0.0

# Fetch real-time data for a specific trading pair and timeframe
symbol = 'BTC/USDT'  # Use the perpetual BTC/USDT contract
timeframe = '1m'  # Use a lower timeframe for real-time streaming, '1m' is just an example
window_size = 10

# Define the leverage for your trades
leverage = 10  # Replace with your desired leverage

# Define the desired risk percentage (e.g., 2%)
risk_percentage = 2

# Initialize the Random Forest Classifier
classifier = RandomForestClassifier()

# Main trading loop
while True:
    try:
        # Fetch real-time data
        real_time_data = fetch_real_time_data(symbol, timeframe)

        if real_time_data is not None:
            # Generate AI indicator on real-time data
            ai_indicator = generate_ai_indicator(real_time_data)

            # Create machine learning dataset
            X, y = create_dataset(real_time_data, window_size)

            # Train the classifier
            classifier.fit(X, y)

            # Make prediction for the next data point
            next_data_point = real_time_data[-window_size:]
            prediction = classifier.predict([next_data_point])[0]

            # Define trading signal based on the prediction
            signal = 'BUY' if prediction == 1 else 'SELL'

            # Get account balance in USDT
            account_balance = get_account_balance()

            # Calculate the trade amount in USDT based on available balance and risk percentage
            risk_amount = (account_balance * risk_percentage) / 100
            trade_amount = min(risk_amount, account_balance)  # Limit trade amount to available balance

            # Print trading signal and trade amount
            print(f"Signal: {signal}, Trade Amount (USDT): {trade_amount:.2f}")

            # Execute the trade
            if signal == 'BUY':
                place_market_order(symbol, 'buy', trade_amount, leverage)
            elif signal == 'SELL':
                place_market_order(symbol, 'sell', trade_amount, leverage)

        # Add a sleep interval to control the trading frequency (e.g., sleep for 1 minute)
        time.sleep(60)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
