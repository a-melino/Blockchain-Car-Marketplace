import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json


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


# Helper functions for pinning
def pin_car_data(name, file):
    ipfs_file_hash = pin_file_to_ipfs(file.getvalue())
    token_json = {
        "name": name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)
    json_ipfs_hash = pin_json_to_ipfs(json_data)
    return json_ipfs_hash, token_json


# Main Streamlit UI
st.title("Query Cars")

query_address = os.getenv("SMART_CONTRACT_ADDRESS");

token_count = contract.functions.totalSupply().call()
st.write(f"token_count: {token_count}")

tokenId = st.selectbox("Select a Token ID:", range(token_count))

if st.button("Fetch Car"):
    st.write(f"{tokenId}")

    

# Fetch total number of cars/tokens
total_cars = contract.functions.totalSupply().call()
car_ids = list(range(total_cars))