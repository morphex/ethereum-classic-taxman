#!/bin/bash

echo "Testing a randomly selected ETC address with few and recent transactions"

./run.py 0x222f266B603e4fa6D5605b5ec1F1C86E35C19F7D 14671157
#Disabled, because CSV file might be missing
#./parse_exchange_rates.py
./generate_csv.py

