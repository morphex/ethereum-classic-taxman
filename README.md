Ethereum (classic) taxman

Program to generate documents suitable for accounting / tax purposes, for
funds received and sent from Ethereum and Ethereum classic addresses.

Connects to a local instance of geth/core-geth to download transactions.

./run.py ADDRESS STARTBLOCK to get started.  It is a good idea to start
at the block prior to the first transaction, as it can take quite a bit of
time to go through all the blocks in each blockchain.

I've built the Ethereum classic database using

/usr/local/bin/core-geth/geth --classic --cache 4096 --datadir \
  /media/morphex/mymedia/morphex/core-geth/data --port 40404

and the Ethereum database using

geth --mainnet --syncmode="snap" --cache 4096

Syncmode snap was the only thing that worked in a satisfying manner when
downloading a copy of the Ethereum database; not many peers support light
mode.

