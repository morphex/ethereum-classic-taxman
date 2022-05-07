#!/usr/bin/python3

import sys
import datetime, time, pytz
from database import initialize_transactions, initialize_blocks, initialize_rates, initialize_rates_fiat
from collections import OrderedDict
from utilities import warning

index, transactions = initialize_transactions()
numbers, blocks = initialize_blocks()
rates = initialize_rates()
rates_fiat = initialize_rates_fiat()

from decimal import Decimal, getcontext
GWEI_DENOMINATOR = Decimal(1000000000.0)
ZERO = Decimal(0.0)
csv_format = lambda x: "%.6f" % x

BLOCK_TIMESTAMP_TIMEZONE = pytz.timezone("UTC")

main_account = ''
receivers = [] #receivers = ['all']
receivers_data = {} #receivers_data = {'all':[]}
value_data = OrderedDict()

accounting_timezone = pytz.timezone("CET")
year = 1970

ignore_hashes = ()

try:
    year = int(sys.argv[1])
except IndexError:
    pass

try:
    # Hashes for failed transactions, ignore value, include fee
    ignore_hashes = tuple(sys.argv[2].split(","))
except IndexError:
    pass




if year == 1970:
    start = datetime.datetime(year, 1, 1,
                              hour=0, minute=0, second=0,
                              tzinfo=accounting_timezone)
    end = datetime.datetime.now(tz=accounting_timezone)
else:
    start = datetime.datetime(year, 1, 1,
                          hour=0, minute=0, second=0,
                          tzinfo=accounting_timezone)
    end = datetime.datetime(year + 1, 1, 1,
                          hour=0, minute=0, second=0,
                          tzinfo=accounting_timezone)

#print(start.timetuple(), end.timetuple())

start = time.mktime(start.timetuple())
end = time.mktime(end.timetuple())
#print(start, end)

fifo_values = OrderedDict()

def peek(ordereddict, index=0):
    x = 0
    for item in ordereddict.items():
        if index == x:
            return item
        x += 1
    else:
        raise IndexError

def calculate_balance(values, hash=None):
    balance = Decimal(0.0)
    for hash, transaction in values.items():
        if transaction[0] == '+':
            balance += transaction[3]
        elif transaction[0] == '-':
            if not hash in ignore_hashes:
                balance -= transaction[3]
            balance -= transaction[4]
    return balance

def calculate_usd_value(values, hash=None):
    copy = values.copy()
    balance = Decimal(0.0)
    for hash, transaction in copy.items():
        if transaction[0] == '+':
            balance += transaction[3]
        elif transaction[0] == '-':
            if not hash in ignore_hashes:
                balance -= transaction[3]
            balance -= transaction[4]
            total = ZERO
            if not hash in ignore_hashes:
                total += transaction[3]
            total += transaction[4]
            transaction_new = None
            for hash_, transaction_ in copy.items():
                if transaction_[3] >= ZERO:
                    if transaction_[3] >= total:
#                        print("Subtracting all")
                        new_value = transaction_[3] - total
                        transaction_new = transaction_[0:3] + (new_value,) + transaction[4:]
                        copy[hash_] = transaction_new
                        break
                    else:
#                        print("Subtracting some")
                        new_value = 0
                        old_value = transaction_[3]
                        transaction_new = transaction_[0:3] + (new_value,) + transaction[4:]
                        copy[hash_] = transaction_new
                        total -= old_value
                else:
                    # Mostly a safeguard, remove later
                    raise ValueError("Transaction value cannot be negative")
    if balance < ZERO:
        print("Warning, balance below zero")
    return balance, copy

def get_fiat_rate(date, recurse=0):
    """Returns the fiat USD-Currency rate for a given date.

    If a rate isn't specified for that date, return the rate for the
    first previous rate available."""
    if not rates_fiat:
        return Decimal(-1)
    try:
        return Decimal(rates_fiat[date])
    except KeyError:
        if recurse > 5:
            warning("Exceeding 5 recursions for %s" % date)
            return Decimal(-1)
        recurse += 1
        year, month, date = map(int, date.split("-"))
        date = datetime.datetime(year, month, date, hour=0, minute=0) - datetime.timedelta(days=1)
        return get_fiat_rate("%02d-%02d-%02d" % (date.year, date.month, date.day), recurse=recurse)

for block, transaction in transactions:
    if not main_account:
        main_account = transaction['to']
    timestamp = blocks[str(block)]['timestamp']
    to = transaction['to']
    if not to in receivers:
        receivers.append(to)
        receivers_data[to] = []
    timestamp_datetime = datetime.datetime.fromtimestamp(timestamp, tz=BLOCK_TIMESTAMP_TIMEZONE).astimezone(accounting_timezone)
    timestamp_date = str(timestamp_datetime.date())
    timestamp_time = str(timestamp_datetime.time())
    value = (Decimal(transaction['value']) / GWEI_DENOMINATOR) / 1000000000
    gas_price_gwei = transaction['gasPrice']
    gas_price_eth = ((Decimal(gas_price_gwei) / GWEI_DENOMINATOR) * 21000) / 1000000000
    try:
        rate = Decimal(rates[timestamp_date][0])
        gas_price_usd = gas_price_eth * rate
        value_usd = value * rate
        try:
            rate_fiat = get_fiat_rate(timestamp_date)
            rate_fiat_converted = rate_fiat * value_usd
        except KeyError:
            print("KeyError", timestamp_date)
            rate_fiat = -1
            rate_fiat_converted = -1
    except KeyError:
        rate = -1
        gas_price_usd = -1
        value_usd = -1
        rate_fiat = -1
        rate_fiat_converted = -1
    balance = "N/A"
    if transaction['to'] == main_account:
        fifo_values[transaction['hash']] = ("+", timestamp_datetime, timestamp_date, value, gas_price_eth, rate)
    elif transaction['from'] == main_account:
        fifo_values[transaction['hash']] = ("-", timestamp_datetime, timestamp_date, value, gas_price_eth, rate)
    balance = calculate_balance(fifo_values)
    balance_usd, value_data = calculate_usd_value(fifo_values)
    if timestamp < start or timestamp > end: continue
    data = (transaction['from'], transaction['to'], transaction['hash'], value,
		value_usd, gas_price_eth, gas_price_usd, gas_price_gwei, block,
		timestamp, timestamp_date, timestamp_time, rate, balance, balance_usd, rate_fiat_converted, rate_fiat)
    receivers_data[to].append(data)
    if transaction['from'] == main_account:
        receivers_data[main_account].append(data)
#    receivers_data['all'].append(data)

for receiver in receivers:
    file = open(receiver+'.csv', 'w')
    file.write(','.join(("From", "To", "Hash", "Value", "Value USD", "GAS Price ETH/ETC", "Gas price USD", "GAS Price Gwei", "Block",
			"Timestamp", "Timestamp date", "Timestamp time", "Exchange rate", "Balance", "Balance USD", "Value fiat", "Fiat rate")) + "\n")
    for transaction in receivers_data[receiver]:
        file.write(','.join(map(str, transaction)) + '\n')
    file.close()

