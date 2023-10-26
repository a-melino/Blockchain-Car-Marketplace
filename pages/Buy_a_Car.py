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
car_id = st.text_input("Enter the Car ID (Token ID)")
sale_price = st.text_input("Enter the Sale Price (in Ether)")
buyer_address = st.text_input("Enter the Buyer's Address")

if st.button("Buy Car"):
    # Call the listCarForSale function in your smart contract
    tx_hash = contract.functions.listCarForSale(car_id, sale_price).transact({'from': your_address})
    
    # Wait for the transaction to be mined
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    # Handle the receipt to check if the listing process was successful
    if receipt.status == 1:
        st.write("Car purchsed successfully.")
    else:
        st.write("Failed to purchase the car.")
          
# Retrieve and display the list of cars available for sale 
def get_cars_for_sale():
    car_ids = []
    total_cars = contract.functions.totalSupply().call()
    
    for car_id in range(total_cars):
        if contract.functions.carCollection(car_id).call()["isForSale"]:
            car_ids.append(car_id)
            
    return car_ids

cars_for_sale = get_cars_for_sale()
