import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
import requests
import json
import pandas as pd
from io import BytesIO

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

# Get Current ETHUSD Price
@st.cache_resource()
def get_ethusd():
    # Create parameterized url
    request_url = "https://api.etherscan.io/api?module=stats&action=ethprice"

    # Submit request and format output
    response_data = requests.get(request_url)

    # Select fact 
    response_content = response_data.json()

    return float(response_content["result"]["ethusd"])

ethusd_rate = get_ethusd()

# Main Streamlit UI
st.title("Generate Sample Listings")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")

sample_used_cars = pd.read_csv(Path("./predictions/data/sample_cleaned_used_cars.csv"))

if st.button("Register Cars Samples"):
    with open(Path("./images/car.jpg"), 'rb') as file:
            file_content = file.read()
            bytes_io = BytesIO(file_content)

    for i in range(len(sample_used_cars)):
        
        # Get engine string to tokenize
        if sample_used_cars["electric"][i] == 1:
            car_engine = f"{sample_used_cars['engine_hp'][i]}HP Electric Motor"
        else:
            car_engine = f"{sample_used_cars['engine_hp'][i]}HP {sample_used_cars['engine_displacement_size'][i]}L {sample_used_cars['engine_cylinders'][i]} Cylinder Engine"

        # Get transmission string to tokenize
        car_transmission = f"{sample_used_cars['transmission_gears'][i]}-Speed {sample_used_cars['transmission_type'][i]}"

        # Get Car Price in ETH
        car_price = sample_used_cars["price"][i]/ethusd_rate

        car_ipfs_hash, carJson = pin_car_data(f"{sample_used_cars['model_year'][i]} {sample_used_cars['brand'][i]} {sample_used_cars['model'][i]}", bytes_io)
        car_uri = f"ipfs://{car_ipfs_hash}"

        tx_hash = contract.functions.registerCar(
            address,
            (
                sample_used_cars["brand"][i],
                sample_used_cars["model"][i],
                int(sample_used_cars["model_year"][i]),
                int(sample_used_cars["kilometers"][i]),
                sample_used_cars["fuel_type"][i],
                car_engine,
                car_transmission,
                int(sample_used_cars["accident"][i]),
                int(sample_used_cars["clean_title"][i]),
                int(car_price),
                True,
                carJson['image']
            ),   
            car_uri
        ).transact({'from': address, 'gas': 1000000})
        
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write(f"Transaction {i} mined Successfully.")

st.markdown("---")


# Fetch total number of cars/tokens
total_cars = contract.functions.totalSupply().call()
car_ids = list(range(total_cars))