# config
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
api_passphrase = os.getenv('API_PASSPHRASE')

initial_investment = 1000
market = 'AMPL-USDT'

# order parameters for stop loss and take profit
# 'multiple' is a multiple of the initial investment
# 'amount' is the fraction of total AMPL tokens
# sum of 'amount' can't be > 1 (thanks KuCoin)
stop_loss = [
    {'multiple': 1, 'amount': 1}
]
take_profit = [
    # {'multiple': 2, 'amount': 0.5},
    # {'multiple': 10, 'amount': 0.5}
]
