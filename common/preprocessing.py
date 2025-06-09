import pandas as pd
from common.dto.Customer import CustomerSchema

def preprocess_data(dataset: pd.DataFrame) -> pd.DataFrame:
    
    """
    Preprocesses a DataFrame whose rows/columns match the CustomerDTO schema.
    Validates the DataFrame using pandera for schema compliance.
    """
    # Validate the DataFrame using pandera
    dataset = CustomerSchema.validate(dataset, lazy=True)

    # Contract is a importnent feature in the model and cant be null, in case of null the model will not predict and need to sand alert.
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

    return dataset