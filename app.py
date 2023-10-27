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
st.title("Car Marketplace")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")


# Register New Property
st.markdown("## Register New Car")
car_name = st.text_input("Enter a name for this car.")
car_brand = st.text_input("Enter the brand of the car.")
car_model = st.text_input("Enter the model of the car.")
car_mileage = st.text_input("Enter the mileage of the car (in miles).")
car_year = st.text_input("Enter the car's model year.")
car_accident = st.selectbox("Has this car been in an accident?", (True, False))
file = st.file_uploader("Upload Car Image.", type=["jpg", "jpeg", "png"])

if st.button("Register Car"):
    car_ipfs_hash, carJson = pin_car_data(car_name, file)
    car_uri = f"ipfs://{car_ipfs_hash}"

    tx_hash = contract.functions.registerCar(
        address,
        car_brand,       
        car_model,           
        int(car_year),       
        int(car_mileage),
        bool(car_accident),   
        carJson['image'],
        car_uri
    ).transact({'from': address, 'gas': 1000000})
    
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.markdown(f"[Car IPFS Gateway Link](https://ipfs.io/ipfs/{car_ipfs_hash})")
    st.markdown(f"[Car IPFS Image Link](https://ipfs.io/ipfs/{carJson['image']})")

st.markdown("---")

# Query Cars Associated with an Address

st.sidebar.subheader("Query Cars by Address")
query_address = st.text_input("Enter Ethereum address to fetch associated Cars")

if st.sidebar.button("Fetch Cars"):
    token_count = contract.functions.balanceOf(query_address).call()
    car_tokens = [contract.functions.tokenOfOwnerByIndex(query_address, i).call() for i in range(token_count)]
    st.sidebar.write(f"Cars associated with address {query_address}:")
    for token in car_tokens:
        token_uri = contract.functions.tokenURI(token).call()
        st.sidebar.write(f"Car ID: {token} - Cars: {car_uri}")


# Fetch total number of cars/tokens
total_cars = contract.functions.totalSupply().call()
car_ids = list(range(total_cars))