#!/usr/bin/python3

import csv
import database
import sys

date_index = 14
value_index = 15

skip_header = True

if skip_header:
    start = 1
else:
    start = 0

rates = database.initialize_rates_fiat()

try:
    datafile = sys.argv[1]
except IndexError:
    datafile = "../USD-NOK.csv"

try:
    delimiter = sys.argv[2]
except IndexError:
    delimiter = ","

try:
    fraction = sys.argv[3]
except IndexError:
    fraction = ","

if fraction == ",":
    parse_float = lambda x: float(x.replace(",", "."))
else:
    parse_float = lambda x: x

try:
    date_order = sys.argv[4]
except IndexError:
    date_order = "ymd"

if date_order == "ydm":
    def reorder_date(date):
        date = date.split("-")
        return date[0] + "-" + date[2] + "-" + date[1]
else:
    reorder_date = lambda x: x

for row in list(csv.reader(open(datafile), delimiter=delimiter))[start:]:
    date = reorder_date(row[date_index])
    value = parse_float(row[value_index])
    rates[date] = value

database.save_rates_fiat(rates)
