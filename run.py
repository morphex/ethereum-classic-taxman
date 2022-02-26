#!/usr/bin/python3

import time
import pickle
import sys
from connection import w3
from utilities import dump_exception

database = "transactions.p"

last_block_index = 0
transactions = []

from database import initialize_transactions, save_transactions

last_block_index, transactions = initialize_transactions()

my_address = sys.argv[1]
index = 0

if not last_block_index:
    try:
        index = int(sys.argv[2])
    except IndexError:
        pass
else:
    print("Found saved work")
    if my_address == transactions[0][1]['to'] or \
       my_address == transactions[0][1]['from']:
        print("Saved work matches CLI argument")
        print("Starting at block %i" % last_block_index)
    else:
        print("Saved work does not match CLI argument")
        sys.exit(1)
    index = last_block_index

start = time.time()

stop = False
count = 0

try:
    while True :
        block_ = hex(index)

        block = w3.eth.get_block(block_, full_transactions=True)
        for transaction in block['transactions']:
            if transaction['to'] == my_address or \
               transaction['from'] == my_address:
                print("Eureka!", index, block_ )
                transactions.append((index, transaction))
        if stop: break
        index += 1
        count += 1
        if not index % 100:
            time_used = time.time() - start
            print(count, block_, time_used, count / time_used)
except KeyboardInterrupt:
    print("Stopping dump of transactions")
except Exception as exception:
    #raise
    print("Stopping dump of transactions")
    dump_exception(exception)

save_transactions(index, transactions)
