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
st.title("Car Marketplace")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
st.markdown("---")


# Register New Car
st.markdown("## Register New Car")

brands = ['Ford', 'Hyundai', 'Lexus', 'INFINITI', 'Audi', 'Acura', 'BMW',
       'Tesla', 'Land', 'Aston', 'Toyota', 'Lincoln', 'Jaguar',
       'Mercedes-Benz', 'Dodge', 'Nissan', 'Genesis', 'Chevrolet', 'Kia',
       'Jeep', 'Bentley', 'Honda', 'Lucid', 'MINI', 'Porsche', 'Hummer',
       'Chrysler', 'Volvo', 'Cadillac', 'Lamborghini', 'Maserati',
       'Volkswagen', 'Subaru', 'Rivian', 'GMC', 'RAM', 'Alfa', 'Ferrari',
       'Scion', 'Mitsubishi', 'Mazda', 'Saturn', 'Bugatti', 'Polestar',
       'Rolls-Royce', 'McLaren', 'Buick', 'Lotus', 'Pontiac', 'FIAT',
       'Karma', 'Saab', 'Mercury', 'Plymouth', 'smart', 'Maybach',
       'Suzuki', 'Other']
car_brand = st.selectbox("Select the brand of the car.", options=brands)
if car_brand == "Other":
    other_car_brand = st.text_input("Enter the brand of the car.")

car_model = st.text_input("Enter the model of the car.")

car_year = st.number_input("Enter the car's model year.", min_value=1900)

car_mileage = st.number_input("Enter the mileage of the car (in kilometers).", min_value=0.0)

car_electric = st.selectbox("Is the car fully electric?", ("No", "Yes"))

if car_electric == "No":
    fuel_types = ['-', 'E85 Flex Fuel', 'Gasoline', 'Hybrid', 'Diesel', 'Plug-In Hybrid']
    car_fuel_type = st.selectbox("Select the fuel type of the car.", options=fuel_types)

    engine_cylinders = ['-', '3', '4', '5', '6', '8', '10', '12', '16']
    car_engine_cylinders = st.selectbox("Select the number of cylinders in the car's engine. (ex. A v6 engine has 6 cylinders)", options=engine_cylinders)

    car_engine_displacement = st.number_input("Enter the displacement size of the engine(in liters)", min_value=0.0, max_value=10.0)
else:
    car_fuel_type = '-'
    car_engine_cylinders = '-'
    car_engine_displacement = 0.0
    
car_engine_hp = st.number_input("Enter the number of HP(Horsepower) the car produces.", min_value=0.0)

# Get engine string to tokenize
if car_electric:
    car_engine = f"{car_engine_hp}HP Electric Motor"
else:
    car_engine = f"{car_engine_hp}HP {car_engine_displacement}L {car_engine_cylinders} Cylinder Engine"

transmission_gears = ['-', '1', '2', '4', '5', '6', '7', '8', '9', '10']
car_transmission_gears = st.selectbox("Select the number of gears the car's transmission has. (ex. A 6-Speed transmission has 6 gears)", options=transmission_gears)

transmission_type = ['-', 'Automatic', 'Manual','CVT', 'DCT']
car_transmission_type = st.selectbox("Select the transmission type of the car.", options=transmission_type)

# Get transmission string to tokenize
car_transmission = f"{car_transmission_gears}-Speed {car_transmission_type}"

car_accident = st.selectbox("Has this car been in an accident?", ("No", "Yes"))

car_clean_title = st.selectbox("Does this car have a clean title? (i.e. Has this car never been deemed a total loss?)", ("No", "Yes"))

file = st.file_uploader("Upload Car Image.", type=["jpg", "jpeg", "png"])

# Get a price recomendation based on the provided information
if st.button("Get Car Listing Price Recomendation"):
    car_data = {
        "brand": car_brand,
        "year": car_year,
        "mileage": car_mileage,
        "electric": car_electric,
        "fuel_type": car_fuel_type,
        "engine_cylinders": car_engine_cylinders,
        "engine_displacement": car_engine_displacement,
        "engine_hp": car_engine_hp,
        "transmission_gears": car_transmission_gears,
        "transmission_type": car_transmission_type,
        "accident": car_accident,
        "clean_title": car_clean_title
    }

    with st.spinner('Please wait while a reccomendation is being calculated...'):
        price_prediction = predict_price(car_data)

    price_prediction_eth = price_prediction/ethusd_rate

    st.success(f"The reccomended listing price for your car is {price_prediction_eth} ETH (${price_prediction} USD)")
else:
    price_prediction_eth = 0.0

car_price = st.number_input("Enter the price you wish to list the car for.(in ETH)", min_value=0.0)

if st.button("Register Car"):
    car_ipfs_hash, carJson = pin_car_data(f"{car_year} {car_brand} {car_model}", file)
    car_uri = f"ipfs://{car_ipfs_hash}"

    if car_accident == "Yes":
        car_accident_value = 1
    else:
        car_accident_value = 0

    if car_clean_title == "Yes":
        car_clean_title_value = 1
    else:
        car_clean_title_value = 0

    tx_hash = contract.functions.registerCar(
        address,
        (
            car_brand,
            car_model,
            car_year,
            int(car_mileage),
            car_fuel_type,
            car_engine,
            car_transmission,
            car_accident_value,
            car_clean_title_value,
            int(car_price),
            True,
            carJson['image']
        ),   
        car_uri
    ).transact({'from': address, 'gas': 1000000})
    
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.markdown(f"[Car IPFS Gateway Link](https://ipfs.io/ipfs/{car_ipfs_hash})")
    st.markdown(f"[Car IPFS Image Link](https://ipfs.io/ipfs/{carJson['image']})")

st.markdown("---")


# Fetch total number of cars/tokens
total_cars = contract.functions.totalSupply().call()
car_ids = list(range(total_cars))