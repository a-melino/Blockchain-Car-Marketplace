import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import json
import joblib
from datetime import datetime

def predict_price(car_data):
    """
    Loads relevant models and objects to make a prediction 
    on the car price with the provided data.
    """
    # Load the model
    model_file_path = Path("predictions/saved_models/gtb_classifier_opt.sav")

    # Load the model to a new object
    gtb_imported = joblib.load(model_file_path)

    # Load the empty prediction
    prediction_file_path = Path("predictions/saved_models/predict.json")

    # Load the empty prediction to a dictionary
    with open(prediction_file_path) as predict_json:
        predict_dict = json.load(predict_json)

    # Turn the prediction dictionary to a DataFrame
    predict_df = pd.DataFrame(predict_dict, index = [0])

    # Load the Standard Scaler
    scaler_file_path = Path("predictions/saved_models/used_cars_scaler.bin")

    # Load the used cars Standard Scaler
    used_cars_scaler =  joblib.load(scaler_file_path) 

    # Parse user input into prediction dictionary
    if car_data["brand"] == "Other":
        pass
    else:
        predict_df["brand_" + car_data["brand"]] = 1

    predict_df["age"] = datetime.now().year - car_data["year"]

    predict_df["kilometers"] = car_data["mileage"]

    if car_data["electric"] == "Yes":
        predict_df["electric"] = 1
    else:
        if car_data['fuel_type'] == "–":
            pass
        else:
            predict_df["fuel_type_" + car_data["fuel_type"]] = 1
        
        if car_data['engine_cylinders'] == "–":
            pass
        else:
            predict_df["engine_cylinders_" + car_data["engine_cylinders"]] = 1
        
        if car_data["engine_displacement"] > 0 and car_data["engine_displacement"] < 3.0:
            predict_df["engine_displacement_small"] = 1
        elif car_data["engine_displacement"] >= 3.0 and car_data["engine_displacement"] < 5.0:
            predict_df["engine_displacement_medium"] = 1 
        elif car_data["engine_displacement"] >= 5.0:
            predict_df["engine_displacement_large"] = 1 
        else:
            pass

    if car_data["engine_hp"] > 0 and car_data["engine_hp"] <= 150:
        predict_df["engine_power_output_low"] = 1
    elif car_data["engine_hp"] > 150 and car_data["engine_hp"] <= 300:
        predict_df["engine_power_output_medium"] = 1
    elif car_data["engine_hp"] > 300:
        predict_df["engine_power_output_high"] = 1
    else:
        pass

    if car_data['transmission_gears'] == "–":
        pass
    else:
        predict_df["transmission_gears_" + car_data["transmission_gears"]] = 1

    if car_data['transmission_type'] == "–":
        pass
    else:
        predict_df["transmission_type_" + car_data["transmission_type"]] = 1

    if car_data["accident"] == "Yes":
        predict_df["accident"] = 1
    else:
        pass

    if car_data["clean_title"] == "Yes":
        predict_df["clean_title"] = 1
    else:
        pass

    # Apply the Standard Scaler to the prediction DataFrame
    predict_scaled = used_cars_scaler.transform(predict_df)

    # Make the prediction using the model
    prediction = gtb_imported.predict(predict_scaled)

    # Return the prediction
    return prediction[0]