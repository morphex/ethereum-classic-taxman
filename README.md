# Ethereum (classic) taxman

Program to generate documents suitable for accounting / tax purposes,
for funds received and sent from Ethereum and Ethereum classic
addresses.

Connects to a local instance of geth/core-geth to download
transactions.

./run.py ADDRESS STARTBLOCK to get started.  It is a good idea to
start at the block prior to the first transaction, as it can take
quite a bit of time to go through all the blocks in each blockchain.

I've built the Ethereum classic database using

/usr/local/bin/core-geth/geth --classic --cache 4096 --datadir \
  /media/morphex/mymedia/morphex/core-geth/data --port 40404

and the Ethereum database using

geth --mainnet --syncmode="snap" --cache 4096

Syncmode snap was the only thing that worked in a satisfying manner
when downloading a copy of the Ethereum database; not many peers
support light mode.

To test if this works, web3 is required, IIRC it is

  pip3 install web3

And to test against a local ETC node, use the command line above as
well as runing ./test.sh

If you want to send me a tip, for example if this saved your bacon, I
have an ETH address

0xFf9df27a4A09C071970487c7568317F8EdcEfcEB

and an ETC address

0x83D06C9B848dD648c257dbe442181A219B6BE391

I'm also available for consulting via my company, obviously I have
some Python experience and blockchain experience, I also know a bit
about web development, system administration etc.

morphex@gmail.com is my email address.

