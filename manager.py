# manager.py
from kucoin.client import Client
import config
import logging
import sys
import math

log_format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
logging.basicConfig(filename='AMPL_manager.log', level=logging.INFO, format=log_format)
client = Client(config.api_key, config.api_secret, config.api_passphrase)


def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def place_order(order, stop=None):
    total_value = config.initial_investment * order['multiple']
    price = truncate(total_value / AMPL_total_qty, 4)
    sell_qty = truncate(AMPL_total_qty * order['amount'], 2)
    if stop:
        stop_price = price
    else:
        stop_price = None
    logging.info(f'New order: {order["multiple"]}x initial value, {sell_qty:.2f}AMPL @ {price:.2f}USD')
    return client.create_limit_order(symbol=config.market, side='sell', price=price,
                                     size=sell_qty, stop=stop, stop_price=stop_price)


# cancel previous orders
client.cancel_all_orders()

# total AMPL
balances = client.get_accounts()
AMPL_balances = [balance for balance in balances if balance['currency'] == 'AMPL']
AMPL_total_qty = sum(float(balance['balance']) for balance in AMPL_balances)
logging.info(f'total balance: {AMPL_total_qty:.2f}')

# AMPL in trading account
AMPL_trading_balance = 0
for AMPL_balance in AMPL_balances:
    if AMPL_balance['type'] == 'trade':
        AMPL_trading_balance = float(AMPL_balance['balance'])
        break
logging.info(f'trading balance: {AMPL_trading_balance:.2f}')

# Checking that AMPL in trading account is sufficient
stop_loss_total = sum(stop_limit_order['amount'] for stop_limit_order in config.stop_loss)
take_profit_total = sum(limit_order['amount'] for limit_order in config.take_profit)
orders_total_qty = (stop_loss_total + take_profit_total) * AMPL_total_qty
logging.info(f'needed for orders: {orders_total_qty:.2f}')
if orders_total_qty > AMPL_trading_balance:
    logging.error('Trading balance is insufficient for orders')
    logging.error('Stopping the program')
    sys.exit()

# Setting stop loss orders
for stop_limit_order in config.stop_loss:
    response = place_order(stop_limit_order, stop='loss')
    logging.info(f'order response: {response}')

# Setting take profit orders
for limit_order in config.take_profit:
    response = place_order(limit_order)
    logging.info(f'order response: {response}')
