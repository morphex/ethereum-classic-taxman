#!/usr/bin/python3

import time
import json
import sys, os
from connection import w3
from utilities import dump_exception
from web3._utils.encoding import Web3JsonEncoder as jsonencoder

transactions_database = "transactions.json"
blocks_database = "blocks.json"
rates_database = "rates.json"

data_backups_dir = "./data_backups/"
temporary_extension = ".tmp"
old_extension = ".old"

last_block_index = 0
transactions = []

try:
    os.mkdir(data_backups_dir)
except FileExistsError:
    # print("Data backup directory already exists")
    pass

def _create_transactions_database():
    with open(transactions_database, "x") as file:
        file.write(json.dumps((last_block_index, transactions), cls=jsonencoder))

def initialize_transactions():
    try:
        f = open(transactions_database, "r")
        last_block_index, transactions = json.loads(f.read())
        #return int(last_block_index), transactions
        return last_block_index, transactions
    except FileNotFoundError:
        _create_transactions_database()
        return initialize_transactions()
    except Exception as exception:
        print("Uknown error in initialization of transactions database")
        dump_exception(exception)
        raise

def save_transactions(index, transactions):
    print("Saving transactions..")
    with open(transactions_database + temporary_extension, "w") as file:
        file.write(json.dumps((index, transactions), cls=jsonencoder))
    os.rename(transactions_database, data_backups_dir + transactions_database + "." + str(time.time()) + old_extension)
    os.rename(transactions_database + temporary_extension, transactions_database)

#initialize_transactions()

numbers = []
blocks = {}

def _create_blocks_database():
    global numbers, blocks
    with open(blocks_database, "x") as file:
        file.write(json.dumps((numbers, blocks), cls=jsonencoder))

def initialize_blocks():
    try:
        f = open(blocks_database, "r")
        numbers, blocks = json.loads(f.read())
        #numbers = list(map(lambda x: int(x), numbers))
        return numbers, blocks
    except FileNotFoundError:
        _create_blocks_database()
        return initialize_blocks()
    except Exception as exception:
        print("Uknown error in initialization of blocks database")
        dump_exception(exception)
        raise

def save_blocks(numbers, blocks):
    print("Saving blocks..")
    numbers.sort()
    # FIXME, rename before save
    with open(blocks_database + temporary_extension, "w") as file:
        file.write(json.dumps((numbers, blocks), cls=jsonencoder))
    os.rename(blocks_database, data_backups_dir + blocks_database + "." + str(time.time()) + old_extension)
    os.rename(blocks_database + temporary_extension, blocks_database)


#initialize_blocks()

rates = {}

def _create_rates_database():
    global rates
    with open(rates_database, "x") as file:
        file.write(json.dumps(rates, cls=jsonencoder))

def initialize_rates():
    try:
        f = open(rates_database, "r")
        rates = json.loads(f.read())
        #for key, value in rates.items():
        #    rates[key] = tuple(map(float, value))
        return rates
    except FileNotFoundError:
        _create_rates_database()
        return initialize_rates()
    except Exception as exception:
        print("Uknown error in initialization of rates database")
        dump_exception(exception)
        raise

def save_rates(rates):
    print("Saving rates..")
    # FIXME, rename before save
    with open(rates_database + temporary_extension, "w") as file:
        file.write(json.dumps(rates, cls=jsonencoder))
    os.rename(rates_database, data_backups_dir + rates_database + "." + str(time.time()) + old_extension)
    os.rename(rates_database + temporary_extension, rates_database)
