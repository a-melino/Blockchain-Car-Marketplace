import os
import json
from web3 import Web3
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Connect to Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI"))

# Load the contract (same as in your previous code)
contract = load_contract()

# User Interface
st.title("Sell a Car")
car_id = st.text_input("Enter the Car ID (Token ID)")
sale_price = st.text_input("Enter the Sale Price (in Ether)")
buyer_address = st.text_input("Enter the Buyer's Address")

if st.button("List Car for Sale"):
    # Call the listCarForSale function in your smart contract
    tx_hash = contract.functions.listCarForSale(car_id, sale_price).transact({'from': your_address})
    
    # Wait for the transaction to be mined
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    # Handle the receipt to check if the listing process was successful
    if receipt.status == 1:
        st.write("Car listed for sale successfully.")
    else:
        st.write("Failed to list the car for sale.")
          
# Retrieve and display the list of cars available for sale 
def get_cars_for_sale():
    car_ids = []
    total_cars = contract.functions.totalSupply().call()
    
    for car_id in range(total_cars):
        if contract.functions.carCollection(car_id).call()["isForSale"]:
            car_ids.append(car_id)
            
    return car_ids

cars_for_sale = get_cars_for_sale()
