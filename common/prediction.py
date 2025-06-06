def predict(rf_model, dataset):
    """
    Predicts the target variable using the provided random forest model and dataset.

    Parameters:
    rf_model (RandomForestClassifier): The trained random forest model.
    dataset (DataFrame): The dataset containing the features for prediction.

    Returns:
    Series: The predicted values.
    """
    # Ensure the dataset contains the required columns
    required_columns = ['TotalCharges', 'Month-to-month', 'One year', 'Two year', 'PhoneService', 'tenure']
    
    if not all(col in dataset.columns for col in required_columns):
        raise ValueError("Dataset must contain the following columns: " + ", ".join(required_columns))
    
    # Select the relevant columns for prediction
    return rf_model.predict(dataset[required_columns])
