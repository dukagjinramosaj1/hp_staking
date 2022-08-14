from web3 import Web3, HTTPProvider
import json
import hashlib
import requests

from urllib.request import urlopen

# to interact with the blockchain
GANACHE = "http://ganache:8545"

MNEMONIC = 'fury theory split solid slam enemy holiday assist ladder point mammal swarm'

web3 =  Web3(Web3.HTTPProvider(GANACHE))
#  Path to the compiled contract JSON file
compiled_contract_path_HMtoken = './blockchain/build/contracts/HMToken.json'
compiled_contract_path_EscrowFactory = './blockchain/build/contracts/EscrowFactory.json'

with open(compiled_contract_path_HMtoken) as file_HMT:
    contract_json_HMT = json.load(file_HMT)  # load contract info as JSON
    contract_abi_HMT = contract_json_HMT['abi']  # fetch contract's abi - necessary to call its functions
    contract_bytecode_HMT = contract_json_HMT['bytecode']

with open(compiled_contract_path_EscrowFactory) as file_Escrow:
    contract_json = json.load(file_Escrow)  # load contract info as JSON
    contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    contract_bytecode = contract_json['bytecode']


# Function for deploying smart contracts
def deployHMToken_Contract():
    print('----------- Deploying HMT Token Contract -----------')

    owner_address = '0x09bb04643ED3F73E4B3998FBb57Fd790296DB558'
    private_key = '0x0af00197abc3998c2353f1c33d2e4287c34336cac54cd10b39fa465e51fe3f16'
    # # # # Fetch deployed contract reference
    contract_instance = web3.eth.contract(abi=contract_abi_HMT, bytecode=contract_bytecode_HMT)


    # nonce is needed to keep track of the account's transactions
    nonce = web3.eth.getTransactionCount(owner_address)  #account that's issuing the transaction

    # estimate_gas = contract_instance .constructor().estimateGas()
    # print("ESTIMATED GAS FOR DEPLOYMENT",estimate_gas)
    # building the Smart Contract deployment transaction
    deploy_txn = contract_instance .constructor(2000000, 'HM Token', 12, 'HMT').buildTransaction({
       'chainId': 1337,
        'gas': 6721975,
        'gasPrice': web3.toWei('7', 'gwei'),
        'nonce': nonce,
    })

    #Signing the transaction with the private key of AFTS
    signed_txn = web3.eth.account.signTransaction(deploy_txn,private_key=private_key)
    #Send the signed transaction as rawTransaction
    send_txn = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    #we wait for the transaction to be mined and get the Receipt back
    txn_receipt = web3.eth.waitForTransactionReceipt(send_txn)
    # print("TXN Receipt", txn_receipt)
    contractAddress = txn_receipt.contractAddress
    # print("CONTRACT Address", contractAddress)
    #Get the transaction Hash from the receipt
    tx_hash = web3.toHex(txn_receipt.transactionHash)
    #returns the transaction hash to be checked on EtherScan
    return contractAddress

# Function for deploying smart contracts
def deployEscrowFactory_Contract(HMTcontractAddress):
    print('-----------DEPLOOOYING ESCROW FACTORY ----------')

    owner_address = '0x09bb04643ED3F73E4B3998FBb57Fd790296DB558'
    private_key = '0x0af00197abc3998c2353f1c33d2e4287c34336cac54cd10b39fa465e51fe3f16'
    # # # # Fetch deployed contract reference
    contract_instance = web3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

    # nonce is needed to keep track of the account's transactions
    nonce = web3.eth.getTransactionCount(owner_address)  #account that's issuing the transaction

    # estimate_gas = contract_instance .constructor().estimateGas()
    # print("ESTIMATED GAS FOR DEPLOYMENT",estimate_gas)
    # building the Smart Contract deployment transaction
    deploy_txn = contract_instance.constructor(Web3.toChecksumAddress(HMTcontractAddress)).buildTransaction({
       'chainId': 1337,
        'gas': 6721975,
        'gasPrice': web3.toWei('7', 'gwei'),
        'nonce': nonce,
    })

    #Signing the transaction with the private key of AFTS
    signed_txn = web3.eth.account.signTransaction(deploy_txn,private_key=private_key)
    #Send the signed transaction as rawTransaction
    send_txn = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    #we wait for the transaction to be mined and get the Receipt back
    txn_receipt = web3.eth.waitForTransactionReceipt(send_txn)
    #Get the transaction Hash from the receipt
    tx_hash = web3.toHex(txn_receipt.transactionHash)
    #returns the transaction hash to be checked on EtherScan
    return tx_hash


def staking(amount):
    
    owner_address = '0x09bb04643ED3F73E4B3998FBb57Fd790296DB558'
    private_key = '0x0af00197abc3998c2353f1c33d2e4287c34336cac54cd10b39fa465e51fe3f16'
    #we need the contract deployment address
    deployed_contract_address = "0x2739de06e898007dc7223c0c622bf1e7d8cef864"

    contract_instance = web3.eth.contract(address=Web3.toChecksumAddress(deployed_contract_address),abi=contract_abi)

    nonce = web3.eth.getTransactionCount(owner_address)  #account that's issuing the transaction
    print("NONCE BEFORE SENDING",nonce)


    # estimate_gas = contract_instance.functions.staking().estimateGas()
    # print("ESTIMATED GAS FOR MINTING PRODUCT TOKEN: ",estimate_gas)
    #We mint baobab tokens BTK by @params:mintBTK_toPicker(PICKER'sPUBLIC ADDRESS, TOKEN_ID, weight, empty byte data call)
    stakingFunction = contract_instance.functions.staking().buildTransaction({
        'chainId': 1337,
        'gas': 6721975,
        'value': web3.toWei(str(amount), 'gwei'),
        'gasPrice': web3.toWei('10', 'gwei'),
        'nonce': nonce,
    })

    #Signing the transaction with the private key of AFTS
    signed_txn = web3.eth.account.signTransaction(stakingFunction, private_key=private_key)
    #Send the signed transaction as rawTransaction
    send_txn = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    #we wait for the transaction to be mined and get the Receipt back
    txn_receipt = web3.eth.waitForTransactionReceipt(send_txn)
    # Get the transaction Hash from the receipt
    tx_hash = web3.toHex(txn_receipt.transactionHash)
    #returns the transaction hash to be checked on EtherScan
    return send_txn.hex()

def escrow(trustedHandlers):
    
    owner_address = '0x09bb04643ED3F73E4B3998FBb57Fd790296DB558'
    private_key = '0x0af00197abc3998c2353f1c33d2e4287c34336cac54cd10b39fa465e51fe3f16'
    
    #we need the contract deployment address
    deployed_contract_address = "0x2739de06e898007dc7223c0c622bf1e7d8cef864"

    contract_instance = web3.eth.contract(address=Web3.toChecksumAddress(deployed_contract_address),abi=contract_abi)

    nonce = web3.eth.getTransactionCount(owner_address)  #account that's issuing the transaction
    # print("",nonce)


    # estimate_gas = contract_instance.functions.staking().estimateGas()
    # print("ESTIMATED GAS FOR MINTING PRODUCT TOKEN: ",estimate_gas)
    # trustedHandles = ['0x189bcD2EF0C0BD0160DAdBb859B15bbDAcee221E', '0x3F22cc5930E169cFbb06879a2a52dcA9E80d817F', '0x935237aF5c0eFb1384e7fBba67b6FeEB9f9559c0', '0xB7e377C31Dffe7075E3CF66c90ea70EA38119830']

    #TODO: Add Comments
    escrowFunction = contract_instance.functions.createEscrow(trustedHandlers).buildTransaction({
        'chainId': 1337,
        'gas': 6721975,
        # 'value': web3.toWei('10', 'gwei'),
        'gasPrice': web3.toWei('10', 'gwei'),
        'nonce': nonce,
    })

    #Signing the transaction with the private key of AFTS
    signed_txn = web3.eth.account.signTransaction(escrowFunction, private_key=private_key)
    #Send the signed transaction as rawTransaction
    send_txn = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    #we wait for the transaction to be mined and get the Receipt back
    txn_receipt = web3.eth.waitForTransactionReceipt(send_txn)
    # Get the transaction Hash from the receipt
    tx_hash = web3.toHex(txn_receipt.transactionHash)
    #returns the transaction hash to be checked on EtherScan
    return send_txn.hex()




# createEscrow = escrow(owner_address, private_key)
# print("CREATED ESCROW", createEscrow)

def get_stakeholder():
    deployed_contract_address = "0x2739de06e898007dc7223c0c622bf1e7d8cef864"

    contractInstance = web3.eth.contract(address=Web3.toChecksumAddress(deployed_contract_address),abi=contract_abi)
    
    stakeholderInstance = contractInstance.functions.stakeholders(0).call()
    # print("STAKEHOLDER IS:", stakeholderInstance)

    return stakeholderInstance

