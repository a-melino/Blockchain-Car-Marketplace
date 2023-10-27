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
    st.write(f"Car ID: {tokenId}")
    st.write(f"Car Owner: {contract.functions.ownerOf(tokenId).call()}")
    st.write(f"Brand: {contract.functions.carCollection(tokenId).call()[0]}")
    st.write(f"Model: {contract.functions.carCollection(tokenId).call()[1]}")
    st.write(f"Year: {contract.functions.carCollection(tokenId).call()[2]}")
    st.write(f"Mileage(in Kilometers): {contract.functions.carCollection(tokenId).call()[3]}")
    st.write(f"Fuel Type: {contract.functions.carCollection(tokenId).call()[4]}")
    st.write(f"Engine: {contract.functions.carCollection(tokenId).call()[5]}")
    st.write(f"Transmission: {contract.functions.carCollection(tokenId).call()[6]}")
    if contract.functions.carCollection(tokenId).call()[7] == 0:
        car_accident = "No"
    else:
        car_accident = "Atleast 1 accident or damage reported."
    st.write(f"Accident: {car_accident}")
    if contract.functions.carCollection(tokenId).call()[8] == 0:
        car_clean_title = "No"
    else:
        car_clean_title = "Yes"
    st.write(f"Accident: {car_accident}")
    st.write(f"Clean TItle: {car_clean_title}")
    st.write(f"Price(in ETH): {contract.functions.carCollection(tokenId).call()[9]}")
    if contract.functions.carCollection(tokenId).call()[10]:
        car_for_sale = "Yes"
    else:
        car_for_sale = "No"
    st.write(f"For Sale: {car_for_sale}")
    car_ipfs_hash = contract.functions.tokenURI(tokenId).call().lstrip("ipfs://")
    st.markdown(f"[Car IPFS Gateway Link](https://ipfs.io/ipfs/{car_ipfs_hash})")
    car_image = contract.functions.carCollection(tokenId).call()[11]
    st.markdown(f"[Car IPFS Image Link](https://ipfs.io/ipfs/{car_image})")

    

# Fetch total number of cars/tokens
total_cars = contract.functions.totalSupply().call()
car_ids = list(range(total_cars))