#!/usr/bin/python3

import sys
import datetime, time, pytz
from database import initialize_transactions, initialize_blocks

index, transactions = initialize_transactions()
numbers, blocks = initialize_blocks()

main_account = ''
receivers = []
receivers_data = {}

timezone = pytz.timezone("CET")
year = 1970

try:
    year = int(sys.argv[1])
except IndexError:
    pass

if year == 1970:
    start = datetime.datetime(year, 1, 1,
                              hour=0, minute=0, second=0,
                              tzinfo=timezone)
    end = datetime.datetime.now(tz=timezone)
else:
    start = datetime.datetime(year, 1, 1,
                          hour=0, minute=0, second=0,
                          tzinfo=timezone)
    end = datetime.datetime(year + 1, 1, 1,
                          hour=0, minute=0, second=0,
                          tzinfo=timezone)

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
    receivers_data[to].append((transaction['from'], transaction['to'], transaction['value'],
				transaction['gas'], transaction['gasPrice'], block, timestamp))

for receiver in receivers:
    file = open(receiver+'.csv', 'w')
    for transaction in receivers_data[receiver]:
        file.write(','.join(map(str, transaction)) + '\n')
    file.close()
