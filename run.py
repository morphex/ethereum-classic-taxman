#!/usr/bin/python3

from web3 import Web3, WebsocketProvider
import time
import pickle
import sys

database = "transactions.p"

last_block_index = 0
transactions = []

def _initialize():
    pickle.dump((last_block_index, transactions), open(database, "wb"))

def initialize():
    try:
        f = open(database, "rb")
        global transactions, last_block_index
        last_block_index, transactions = pickle.load(f)
    except OSError:
        _initialize()
        initialize()

initialize()

w3 = Web3(WebsocketProvider('ws://localhost:8546'))
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

#latest = w3.eth.get_block("latest")
#print ("Latest Ethereum block" , latest)

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
except:
    raise
    print("Stopping dump of transactions")
    print("Stopping dump, unknown error")

print("Saving..")

pickle.dump((index, transactions), open("transactions.p", "wb"))
