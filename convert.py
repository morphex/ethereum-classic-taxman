#!/usr/bin/python3

import database_old
import json

index, transactions = database_old.initialize_transactions()
numbers, blocks = database_old.initialize_blocks()
rates = database_old.initialize_rates()

from web3._utils.encoding import Web3JsonEncoder as jsonencode

with open("transactions.json", "w") as file:
    data = json.dumps((index, transactions), cls=jsonencode)
    file.write(data)
with open("blocks.json", "w") as file:
    file.write(json.dumps((numbers, blocks), cls=jsonencode))
with open("rates.json", "w") as file:
    file.write(json.dumps(rates, cls=jsonencode))
