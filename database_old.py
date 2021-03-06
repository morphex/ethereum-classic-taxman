#!/usr/bin/python3

import time
import pickle
import sys
from connection import w3
from utilities import dump_exception

transactions_database = "transactions.p"
blocks_database = "blocks.p"
rates_database = "rates.p"

last_block_index = 0
transactions = []

def _create_transactions_database():
    pickle.dump((last_block_index, transactions), open(transactions_database, "wb"))

def initialize_transactions():
    try:
        f = open(transactions_database, "rb")
        last_block_index, transactions = pickle.load(f)
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
    # FIXME, rename before save
    pickle.dump((index, transactions), open(transactions_database, "wb"))

#initialize_transactions()

numbers = []
blocks = {}

def _create_blocks_database():
    global numbers, blocks
    pickle.dump((numbers, blocks), open(blocks_database, "wb"))

def initialize_blocks():
    try:
        f = open(blocks_database, "rb")
        numbers, blocks = pickle.load(f)
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
    pickle.dump((numbers, blocks), open(blocks_database, "wb"))

#initialize_blocks()

rates = {}

def _create_rates_database():
    global rates
    pickle.dump(rates, open(rates_database, "wb"))

def initialize_rates():
    try:
        f = open(rates_database, "rb")
        rates = pickle.load(f)
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
    pickle.dump(rates, open(rates_database, "wb"))
