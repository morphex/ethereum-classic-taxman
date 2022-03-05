#!/usr/bin/python3

import csv
import database

# This is a configuration for a CSV file containing the high and low
# points of a cryptocurrency for a given day, in this way
#
# Date,Open,High,Low (Index 0, 1, 2, 3).
#
# According to the Norwegian tax authorities, it is OK to value a
# crypto currency by an average of the highest and lowest rate for a
# given day.

# If that principle is used consistently for all incoming transactions
# for a given year, where the value of the crypto currency hadn't been
# agreed upon at the time of the transaction, for example when
# receiving a reward of some kind or a tip without initiating the
# transaction.

date_index = 0
high_index = 2
low_index = 3

skip_header = True

if skip_header:
    start = 1
else:
    start = 0

rates = database.initialize_rates()

for row in list(csv.reader(open("../etc-usd.csv")))[start:]:
    date = row[date_index]
    high = float(row[high_index])
    low = float(row[low_index])
    rates[date] = ((high + low) / 2, high, low)

database.save_rates(rates)


