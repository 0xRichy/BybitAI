# BybitAI

BybitAI is a high-frequency trading bot for the Bybit derivatives exchange. It uses a simple machine learning model to make trading decisions based on real-time market data.

## Features

- Fetches real-time market data from Bybit
- Generates trading signals using a simple machine learning model
- Places market orders based on the trading signals
- Implements dynamic risk management
- Logs all trading activities and sends them to a Telegram chat

## Installation

1. Clone this repository:

```bash
git clone https://github.com/0xRichy/BybitAI.git
cd BybitAI
```

2. Install the required Python packages:

```bash
pip install ccxt numpy keras python-dotenv python-telegram-bot
```

3. Create a `.env` file in the root directory of the project and add your Bybit API keys and Telegram Bot API token and chat_id:

```env
BYBIT_API_KEY=your_api_key
BYBIT_SECRET_KEY=your_secret_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## Usage

1. Run the main script:

```bash
python main.py
```

The bot will start fetching real-time market data, generating trading signals, and placing market orders based on the signals. All trading activities will be logged and sent to the specified Telegram chat.

## Disclaimer

This bot is for educational purposes only. Do not risk money which you are afraid to lose. USE THE BOT AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.

---

Please note that this is a rough sketch and you'll need to fill in the details yourself. Also, remember to replace the placeholders in the `.env` file with your actual API keys and other environment variables.
