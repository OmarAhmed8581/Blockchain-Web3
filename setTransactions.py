from web3 import Web3
from solcx import compile_source
from solcx import compile_standard, install_solc


install_solc(version='latest')





# Solidity source code
compiled_sol = compile_source(
 '''
pragma solidity >0.5.0;

    contract Greeter {
     string public greeting;

         constructor() public {
             greeting = 'Hello';
         }

         function setGreeting(string memory _greeting) public {
             greeting = _greeting;
         }

         function greet() view public returns (string memory) {
             return greeting;
         }
     }
     ''',
     output_values=['abi', 'bin']
)

contract_id, contract_interface = compiled_sol.popitem()

# get bytecode / bin
bytecode = contract_interface['bin']

# get abi
abi = contract_interface['abi']

# web3.py instance
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

# set pre-funded account as sender
w3.eth.default_account = w3.eth.accounts[1]


Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
tx_hash = Greeter.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

greeter = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)

print(greeter.functions.greet().call())


tx_hash = greeter.functions.setGreeting('Nihao').transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(greeter.functions.greet().call())


