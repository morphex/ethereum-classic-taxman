#!/usr/bin/python3

import sys, os
sys.path.append(os.getcwd())

from connection import w3
from database import initialize_transactions, initialize_blocks, save_blocks

db_index, transactions = initialize_transactions()

print(db_index, len(transactions))

numbers, blocks = initialize_blocks()

print(numbers, len(blocks))

import web3.types
HexBytes = web3.types.HexBytes

for index in range(len(transactions)):
    block_number, transaction = transactions[index]
    for transaction_ in blocks[str(block_number)]['transactions']:
        if transaction['hash'] == transaction_['hash']:
            print("Eureka!")
            print(transaction_)
            w3.eth.get_transaction_receipt(transaction['hash'])
            sys.exit(0)
        else:
            print("No ",)

#save_transactions(db_index, transactions)
