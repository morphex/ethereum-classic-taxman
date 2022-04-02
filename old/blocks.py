#!/usr/bin/python3

import sys, os
sys.path.append(os.getcwd())

from connection import w3
from database import initialize_transactions, initialize_blocks, save_blocks

index, transactions = initialize_transactions()

print(index, len(transactions))

numbers, blocks = initialize_blocks()

print(numbers, len(blocks))

for block_number, transaction in transactions:
    if not block_number in numbers:
        print("Saving block", block_number, numbers)
        block = w3.eth.get_block(hex(block_number))
        blocks[block_number] = block
        numbers.append(block_number)

save_blocks(numbers, blocks)
