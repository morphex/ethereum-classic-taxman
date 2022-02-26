#!/usr/bin/python3

from database import initialize_transactions, initialize_blocks

index, transactions = initialize_transactions()
numbers, blocks = initialize_blocks()

main_account = ''
receivers = []
receivers_data = {}

print(transactions)
for block, transaction in transactions:
    if not main_account:
        main_account = transaction['to']
    to = transaction['to']
    if not to in receivers:
        receivers.append(to)
        receivers_data[to] = []
    receivers_data[to].append((transaction['from'], transaction['to'], transaction['value'],
				transaction['gas'], transaction['gasPrice'], block, blocks[block]['timestamp']))

for receiver in receivers:
    file = open(receiver+'.csv', 'w')
    for transaction in receivers_data[receiver]:
        file.write(','.join(map(str, transaction)) + '\n')
    file.close()
