# BybitAI 🤖 - Automated Cryptocurrency Trading with LSTM Model (Linux 20.04)

Welcome to BybitAI 🤖, your very own automated cryptocurrency trading bot powered by an LSTM model! With this setup running smoothly on your Linux 20.04 VPS, you're about to embark on an exciting journey into the world of crypto trading. Let's dive in:

## What is BybitAI 🤖?

BybitAI 🤖 is an intelligent trading bot designed to handle cryptocurrency trading on the Bybit exchange automatically. Powered by LSTM models and advanced technical indicators, it makes informed trading decisions on your behalf, so you can sit back and enjoy the ride!

## Getting Started

To get started with BybitAI 🤖, follow these simple steps:

1. **Set Up Your Linux 20.04 VPS**: Don't have your Linux VPS ready yet? No worries! We'll guide you through the setup process.

2. **Clone the Repository**: Clone the BybitAI 🤖 repository to your Linux VPS using this command:
   ```bash
   git clone https://github.com/your_username/BybitAI.git
   ```

3. **Install Dependencies**: Move into the project directory and install all the required dependencies:
   ```bash
   cd BybitAI
   pip install -r requirements.txt
   ```

4. **API Credentials**: Grab your Bybit API key and secret from your account dashboard. Once you have them, insert these credentials into the BybitAI.py code to enable trading.

## How Does BybitAI 🤖 Work?

BybitAI 🤖 employs a sophisticated trading strategy that combines the power of LSTM models with advanced technical indicators. Here's a sneak peek at how it works:

1. **Collecting Market Data**: BybitAI 🤖 fetches historical price data for the BTCUSD trading pair from Bybit, using a 1-minute interval for precise analysis.

2. **Indicator Insights**: The bot calculates crucial technical indicators like MACD, RSI, and Bollinger Bands based on the historical price data.

3. **Data Preparation**: To feed the LSTM model, the price data undergoes skillful preprocessing and normalization. BybitAI 🤖 creates sequences of 60 previous data points as inputs for the model.

4. **LSTM Training**: The LSTM model undergoes training using the prepared data to predict future price movements with remarkable accuracy.

5. **Smart Trading Decisions**: Based on the indicators and LSTM predictions, BybitAI 🤖 identifies optimal buy and sell signals for potential trades.

6. **It's Trading Time**: When promising signals arise, the bot executes market orders on Bybit with a quantity of 1 BTC and the leverage you specified.

## Running BybitAI 🤖

Excited to start trading with BybitAI 🤖? Run the bot's Python script using this command:
```bash
python BybitAI.py
```

Remember, BybitAI 🤖 is an educational tool and a starting point for your trading journey. Always implement risk management measures and thoroughly test the strategy with historical data before considering live trading.

## Risk Warning

Trading cryptocurrencies carries inherent risks. Trade responsibly and be mindful of potential losses before making any trading decisions.

May BybitAI 🤖 bring you profitable trades and memorable experiences on your Linux 20.04 VPS! 🚀🐧
