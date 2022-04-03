#!/usr/bin/python3

import sys
import datetime, time, pytz
from database import initialize_transactions, initialize_blocks, initialize_rates

index, transactions = initialize_transactions()
numbers, blocks = initialize_blocks()
rates = initialize_rates()

from decimal import Decimal
GWEI_DENOMINATOR = Decimal(1000000000.0)

BLOCK_TIMESTAMP_TIMEZONE = pytz.timezone("UTC")

main_account = ''
receivers = []
receivers_data = {}

accounting_timezone = pytz.timezone("CET")
year = 1970

try:
    year = int(sys.argv[1])
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

for block, transaction in transactions:
    if not main_account:
        main_account = transaction['to']
    timestamp = blocks[str(block)]['timestamp']
    if timestamp < start or timestamp > end: continue
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
    except KeyError:
        rate = -1
        gas_price_usd = -1
        value_usd = -1
    receivers_data[to].append((transaction['from'], transaction['to'], transaction['hash'], value,
				value_usd, gas_price_eth, gas_price_usd, gas_price_gwei, block,
				timestamp, timestamp_date, timestamp_time, rate))

for receiver in receivers:
    file = open(receiver+'.csv', 'w')
    file.write(','.join(("From", "To", "Hash", "Value", "Value USD", "GAS Price ETH", "Gas price USD", "GAS Price Gwei", "Block",
			"Timestamp", "Timestamp date", "Timestamp time", "Exchange rate")) + "\n")
    for transaction in receivers_data[receiver]:
        file.write(','.join(map(str, transaction)) + '\n')
    file.close()
