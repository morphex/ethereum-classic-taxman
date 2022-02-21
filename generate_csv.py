#!/usr/bin/python3

import pickle

transactions = pickle.load(open("transactions.p", "rb"))
main_account = ''
receivers = []
receivers_data = {}
for block, transaction in transactions[1]:
    if not main_account:
        main_account = transaction['to']
    to = transaction['to']
    if not to in receivers:
        receivers.append(to)
        receivers_data[to] = []
    receivers_data[to].append((transaction['from'], transaction['to'], transaction['value'],
				transaction['gas'], transaction['gasPrice']))

for receiver in receivers:
    file = open(receiver+'.csv', 'w')
    for transaction in receivers_data[receiver]:
        file.write(','.join(map(str, transaction)) + '\n')
    file.close()