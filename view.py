#!/usr/bin/python3

import pprint, sys, json

# Little tool for viewing JSON data / making it easier to edit.
#
# For example
#
# ./view.py transactions.json | less
#
# or
#
# ./view.py transactions.json > transactions_edit.json
# nano transactions_edit.json

pp = pprint.PrettyPrinter()

try:
    datafile = open(sys.argv[1])
except IndexError:
    print(sys.argv[0], "<filename>")
    sys.exit(1)

data = json.loads(datafile.read())
pp.pprint(data)
