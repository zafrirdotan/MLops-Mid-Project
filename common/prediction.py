import pandas as pd
import logging

from sklearn.ensemble import RandomForestClassifier

def predict(rf_model: RandomForestClassifier, dataset: pd.DataFrame) -> pd.Series:
    # Ensure the dataset contains the required columns
    required_columns = ['TotalCharges', 'Month-to-month', 'One year', 'Two year', 'PhoneService', 'tenure']
    
    if not all(col in dataset.columns for col in required_columns):
        logging.error("Dataset is missing required columns for prediction.")
        raise ValueError("Dataset must contain the following columns: " + ", ".join(required_columns) 
                         + ". But it is missing: " + ", ".join(set(required_columns) - set(dataset.columns)))
    
    # Select the relevant columns for prediction
    return rf_model.predict(dataset[required_columns])
