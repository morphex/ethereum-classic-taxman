#!/usr/bin/python3

import time

STARTUP_TIME = time.time()

import sys
from connection import w3
from utilities import dump_exception

last_block_index = 0
transactions = []

from database import initialize_transactions, save_transactions, initialize_blocks, save_blocks

last_block_index, transactions = initialize_transactions()
block_numbers, blocks = initialize_blocks()

my_address = sys.argv[1]
index = 0

if not last_block_index:
    #print((last_block_index,))
    #sys.exit()
    try:
        index = int(sys.argv[2])
    except IndexError:
        pass
else:
    print("Found saved work")
    if transactions:
        if my_address == transactions[0][1]['to'] or \
           my_address == transactions[0][1]['from']:
            print("Saved work matches CLI argument")
            print("Starting at block %i" % last_block_index)
        else:
            print("Saved work does not match CLI argument")
            sys.exit(1)
        index = last_block_index
    else:
        try:
            index = int(sys.argv[2])
        except IndexError:
            pass


start = time.time()

stop = False
count = 0

def save_progress():
    print("Saving progress.. ")
    save_transactions(index, transactions)
    save_blocks(block_numbers, blocks)
    print("Done.")

try:
    while True :
        block_ = hex(index)
        #print(index, block_)
        block = w3.eth.get_block(block_, full_transactions=True)
        for transaction in block['transactions']:
            if transaction['to'] == my_address or \
               transaction['from'] == my_address:
                print("Eureka!", index, block_ )
                transactions.append((index, transaction))
                if index not in block_numbers:
                    block_numbers.append(index)
                    blocks[str(index)] = block
        if stop: break
        index += 1
        count += 1
        if not index % 100:
            time_used = time.time() - start
            print(count, block_, time_used, count / time_used)
        if not index % 50000:
            save_progress()
except KeyboardInterrupt:
    print("Stopping dump of transactions")
except Exception as exception:
    #raise
    print("Stopping dump of transactions")
    dump_exception(exception)

save_progress()
