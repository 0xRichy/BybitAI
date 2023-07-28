import bybit
import pandas as pd
import talib
import time
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Initialize Bybit API
client = bybit.bybit(test=True, api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")

# Define leverage
leverage = 50

# Initialize LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(60,1)))
model.add(LSTM(units=50))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

# Initialize MinMaxScaler
scaler = MinMaxScaler()

# Trading logic
while True:
    # Get historical price data
    data = client.Kline.Kline_get(symbol="BTCUSD", interval="1", limit=500).result()[0]['result']
    data = pd.DataFrame(data)
    data['close'] = data['close'].astype(float)

    # Calculate indicators
    data['macd'], data['macdsignal'], data['macdhist'] = talib.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    data['rsi'] = talib.RSI(data['close'], timeperiod=14)
    data['upperband'], data['middleband'], data['lowerband'] = talib.BBANDS(data['close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

    # Prepare data for LSTM model
    inputs = data['close'].values
    inputs = inputs.reshape(-1,1)
    inputs = scaler.fit_transform(inputs)

    X_train = []
    y_train = []
    for i in range(60, len(inputs)):
        X_train.append(inputs[i-60:i, 0])
        y_train.append(inputs[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Train LSTM model
    model.fit(X_train, y_train, epochs=1, batch_size=1, verbose=2)

    # Predict next price
    X_test = inputs[-60:]
    X_test = np.reshape(X_test, (1, X_test.shape[0], 1))
    predicted_price = model.predict(X_test)
    predicted_price = scaler.inverse_transform(predicted_price)

    # Check for buy signal
    if data['macd'].iloc[-1] > data['macdsignal'].iloc[-1] and data['rsi'].iloc[-1] < 30 and predicted_price > data['close'].iloc[-1]:
        # Place buy order
        client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Market", qty=1, time_in_force="GoodTillCancel", leverage=leverage)
        print("Buy order placed!")
    
    # Check for sell signal
    elif data['macd'].iloc[-1] < data['macdsignal'].iloc[-1] and data['rsi'].iloc[-1] > 70 and predicted_price < data['close'].iloc[-1]:
        # Place sell order
        client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Market", qty=1, time_in_force="GoodTillCancel", leverage=leverage)
        print("Sell order placed!")
    
    # Wait before checking for new signals
    time.sleep(60)
