# BybitAI - Automated Trading Bot with Machine Learning

BybitAI is an automated trading bot that leverages machine learning to make real-time trading decisions on the Bybit derivatives exchange. The bot uses historical market data to generate an AI indicator and makes trading decisions based on the AI indicator and risk management settings.

**Note:** This trading bot is for educational and informational purposes only. Use it at your own risk and do not use it with real funds until you thoroughly understand its operation and have tested it in a simulated environment.

## Getting Started

To run the BybitAI trading bot on your local machine or VPS, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/0xRichy/BybitAI.git
   ```

2. Install required dependencies:
   ```bash
   pip3 install ccxt numpy scikit-learn
   ```

3. Update API Credentials:
   - Open `BybitAI.py` using a text editor.
   - Replace `'YOUR_API_KEY'` and `'YOUR_SECRET_KEY'` with your Bybit API credentials.

4. Run the trading bot:
   ```bash
   python3 BybitAI.py
   ```

**Important:** Before running the bot with real funds, thoroughly test it in a simulated environment and ensure proper risk management strategies are in place.

## Functionality

The BybitAI trading bot performs the following actions:

- Fetches real-time market data from Bybit API.
- Generates an AI indicator based on historical data (currently a simple moving average).
- Creates a machine learning dataset for training a Random Forest Classifier.
- Makes trading decisions based on the AI indicator and risk management settings.
- Places market orders (BUY/SELL) on the BTC/USDT perpetual contract with the specified leverage.

## Configuration

You can customize the bot's behavior by modifying the following variables in `BybitAI.py`:

- `bybit_api_key`: Replace with your Bybit API key.
- `bybit_secret_key`: Replace with your Bybit secret key.
- `symbol`: Trading pair symbol (default: 'BTC/USDT').
- `timeframe`: Timeframe for real-time streaming (default: '1m').
- `window_size`: Number of data points used for AI indicator and machine learning dataset (default: 10).
- `leverage`: Leverage for your trades (default: 10).
- `risk_percentage`: Desired risk percentage for each trade (default: 2).

## Disclaimer

Trading cryptocurrency involves risks, and this trading bot may not guarantee profits. It is crucial to understand the risks associated with trading and only invest what you can afford to lose. The authors of this project are not responsible for any financial losses incurred by using this trading bot.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Please replace `'YOUR_API_KEY'` and `'YOUR_SECRET_KEY'` in `BybitAI.py` with your actual Bybit API credentials before pushing the changes to your GitHub repository.

Feel free to further customize the README to provide additional information, such as the trading strategy employed, performance metrics, and other relevant details about your project. A clear and informative README helps users understand your project and encourages contributions and collaboration.
