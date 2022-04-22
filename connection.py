#!/usr/bin/python3

from web3 import Web3, WebsocketProvider

w3 = Web3(WebsocketProvider('ws://192.168.1.111:8546', websocket_timeout=60))
