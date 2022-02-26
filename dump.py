#!/usr/bin/python3

import database

index, transactions = database.initialize_transactions()
numbers, blocks = database.initialize_blocks()

print(numbers, blocks)
