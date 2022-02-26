#!/usr/bin/python3

import time
import pickle
import sys
from connection import w3
from utilities import dump_exception

transactions_database = "transactions.p"
blocks_database = "blocks.p"

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
        initialize_transactions()
    except Exception as exception:
        print("Uknown error in initialization of transactions database")
        dump_exception(exception)

def save_transactions(index, transactions):
    print("Saving..")
    # FIXME, rename before save
    pickle.dump((index, transactions), open(transactions_database, "wb"))

initialize_transactions()

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
        initialize_blocks()
    except Exception as exception:
        print("Uknown error in initialization of blocks database")
        dump_exception(exception)

def save_blocks(numbers, blocks):
    print("Saving..")
    # FIXME, rename before save
    pickle.dump((numbers, blocks), open(blocks_database, "wb"))

initialize_blocks()
