import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
import requests
import json
from prediction import predict_price
from wallet import get_balance

# Load environment variables
load_dotenv()

# Connect to Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Load the contract
@st.cache_resource()
def load_contract():
    with open(Path('./contracts/compiled/car-marketplace-abi.json')) as f:
        contract_abi = json.load(f)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    return w3.eth.contract(address=contract_address, abi=contract_abi)
contract = load_contract()

# User Interface
st.title("Buy a Car")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.write(f"Account Balance: {get_balance(w3, address)} ETH")
          
# Retrieve and display the list of cars available for sale 
def get_cars_for_sale():
    car_ids = []
    total_cars = contract.functions.totalSupply().call()
    
    for car_id in range(total_cars):
        if contract.functions.carCollection(car_id).call()[-2]:
            car_ids.append(car_id)
            
    return car_ids

cars_for_sale = get_cars_for_sale()

car_id = st.selectbox("Select Car ID to Purchase(Token ID)", options=cars_for_sale)

if st.button("Buy Car"):
    car_price = contract.functions.carCollection(car_id).call()[-3]

    # Call the purchaseCar function in your smart contract
    tx_hash = contract.functions.purchaseCar(car_id).transact({'from': address, 'gas': 1000000, "value": w3.toWei(car_price, "ether")})
    
    # Wait for the transaction to be mined
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    # Handle the receipt to check if the listing process was successful
    if receipt.status == 1:
        st.write("Car purchsed successfully.")
    else:
        st.write("Failed to purchase the car.")