#!/usr/bin/python3

import sys
import datetime, time, pytz
from database import initialize_transactions, initialize_blocks, initialize_rates

index, transactions = initialize_transactions()
numbers, blocks = initialize_blocks()
rates = initialize_rates()

main_account = ''
receivers = []
receivers_data = {}

accounting_timezone = pytz.timezone("CET")
block_timestamp_timezone = pytz.timezone("UTC")
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
    timestamp = blocks[block]['timestamp']
    if timestamp < start or timestamp > end: continue
    to = transaction['to']
    if not to in receivers:
        receivers.append(to)
        receivers_data[to] = []
    timestamp_datetime = datetime.datetime.fromtimestamp(timestamp, tz=block_timestamp_timezone).astimezone(accounting_timezone)
    timestamp_date = str(timestamp_datetime.date())
    timestamp_time = str(timestamp_datetime.time())
    try:
        rate = rates[timestamp_date][0]
    except KeyError:
        rate = -1
    receivers_data[to].append((transaction['from'], transaction['to'], transaction['value'],
				transaction['gas'], transaction['gasPrice'], block, timestamp,
				timestamp_date, timestamp_time, rate))

for receiver in receivers:
    file = open(receiver+'.csv', 'w')
    for transaction in receivers_data[receiver]:
        file.write(','.join(map(str, transaction)) + '\n')
    file.close()
