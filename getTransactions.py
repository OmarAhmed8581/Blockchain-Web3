

from web3 import Web3, HTTPProvider
import pickle
from eth_account import Account
import secrets
w3 = Web3(HTTPProvider('HTTP://127.0.0.1:7545'))
# print ("Latest Ethereum block number" , w3.eth.block_number)



blockchain_address = w3.eth.accounts[0]


w3.eth.default_account = w3.eth.accounts[0]

ending_blocknumber = w3.eth.blockNumber

# latest block number minus 100 blocks
starting_blocknumber = 1 

# filter through blocks and look for transactions involving this address


# create an empty dictionary we will add transaction data to
tx_dictionary = {}


def getTransactions(start, end, address):
    '''This function takes three inputs, a starting block number, ending block number
    and an Ethereum address. The function loops over the transactions in each block and
    checks if the address in the to field matches the one we set in the blockchain_address.
    Additionally, it will write the found transactions to a pickle file for quickly serializing and de-serializing
    a Python object.'''
    print(f"Started filtering through block number {start} to {end} for transactions involving the address - {address}...")
    for x in range(start, end):
        block = w3.eth.getBlock(x, True)
        for transaction in block.transactions:
            if transaction['to'] == address or transaction['from'] == address:
                with open("transactions.pkl", "wb") as f:
                    hashStr = transaction['hash'].hex()
                    tx_dictionary[hashStr] = transaction
                    pickle.dump(tx_dictionary, f)
                   
                f.close()
    print(tx_dictionary)
    print(f"Finished searching blocks {start} through {end} and found {len(tx_dictionary)} transactions")

getTransactions(starting_blocknumber, ending_blocknumber, blockchain_address)



