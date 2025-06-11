import pandas as pd
from common.dto.Customer import CustomerSchema
import logging

def preprocess_data(dataset: pd.DataFrame) -> pd.DataFrame:
    
    """
    Preprocesses a DataFrame whose rows/columns match the CustomerDTO schema.
    Validates the DataFrame using pandera for schema compliance.
    """
    # Validate the DataFrame using pandera, with logging
    try:
        dataset = CustomerSchema.validate(dataset, lazy=True)
        logging.info("DataFrame validation successful.")
    except Exception as e:
        logging.error(f"DataFrame validation failed: {e}")
        raise ValueError(f"DataFrame validation failed: {e}")
    
    # Contract is a importnent feature in the model and cant be null, in case of null the model will not predict and need to sand alert.

    # Check for missing 'Contract' values, log and drop those rows (include customerID in log)
    if dataset['Contract'].isnull().any():
        missing_ids = dataset.loc[dataset['Contract'].isnull(), 'customerID'].tolist()
        missing_count = len(missing_ids)
        logging.error(f"'Contract' column has {missing_count} missing values for customerIDs: {missing_ids}. Dropping these rows.")
        dataset['Contract'] = dataset['Contract'].dropna()
    

    dataset['PhoneService'].fillna('No')
    dataset['tenure'].fillna(dataset['tenure'].mean())

    # Feature handling:
    dataset['PhoneService'] = dataset['PhoneService'].map({'Yes': 1, 'No': 0})

    # One-hot encode Contract and ensure all expected columns exist
    contract_dummies = pd.get_dummies(dataset['Contract']).astype(int)
    for col in ['Month-to-month', 'One year', 'Two year']:
        if col not in contract_dummies:
            contract_dummies[col] = 0

    contract_dummies = contract_dummies[['Month-to-month', 'One year', 'Two year']]
    dataset = dataset.join(contract_dummies)

    logging.info("Preprocessing completed successfully.")

    
    return dataset