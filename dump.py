#!/usr/bin/python3

import pickle

transactions = pickle.load(open("transactions.p", "rb"))
print(len(transactions[1]))
print(transactions)
