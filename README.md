
# Blockchain Car Marketplace

## **Team 2 - Project 3**

### Andy Vu
### Sophie-Pearl Degain 
### Abili Onyepunuka
### Alex Melino
#
#

## **Overview**

For the capstone Fintech project, we have decided to create a car marketplace hosted on the Ethereum blockchain which also incorporates machine learning. The marketplace will allow for a user to register a car to be sold (with a photo), view a list of currently available cars for purchase, and purchase a car. 

In addition, when registering a car for sale, the user will have the ability to call on a pre-trained machine learning model to provide a recommendation for what the sale price should be. 

The machine learning model is trained on a dataset of information and prices of over 4000 used cars (dataset obtained from https://www.kaggle.com, dataset populated with data from https://www.cars.com). 

The backend of the project uses Ganache to generate the Etheruem sandbox in which the smart contract is deployed. The smart contract was deployed using Remix Ethereum IDE, and the front-end of the application is run with Streamlit.
#
#

## **Repository Structure**

The strealit application is executed by running the *'Home_Page.py'* file. The additional pages of the streamlit application each have their own .py file located in the *'pages'* folder.

The smart contract can be found in the *'contracts'* folder under the name *'car-marketplace.sol'*. 

The machine learning Jupyter Notebook file can be found in the *'predictions'* folder under the name *'used_cars_price_prediction.ipynb'*. Also, the model itself can be found in the *'saved_models'* folder, and the *'prediction.py'* file in the main folder contains the predictive machine learning function.
#
#

## **Machine Learning**

The machine learning model used in this project is trained on a dataset of information and prices of over 4000 used cars. The dataset was obtained from https://www.kaggle.com, and the dataset is populated with data from https://www.cars.com. 

The dataset was cleaned, encoded, split into training and testing sets, and then used to evaluate the effectiveness of various machine learning models.

The machine learning model which produced the best results was the Gradient Boosting Regressor. The model was then saved to be used by the *'prediction.py'* This file defines the predictive function which is used by the front-end Streamlit application.
#
#


## **Smart Contract**



#
#