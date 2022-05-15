#!/usr/bin/python3

import pprint, sys, json

pp = pprint.PrettyPrinter()

try:
    datafile = open(sys.argv[1])
except IndexError:
    print(sys.argv[0], "<filename>")
    sys.exit(1)

data = json.loads(datafile.read())
pp.pprint(data)
