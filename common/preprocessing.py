import pandas as pd

def preprocess_data(dataset: pd.DataFrame) -> pd.DataFrame:
    # Ensure TotalCharges is string before replacing spaces
    dataset['TotalCharges'] = dataset['TotalCharges'].astype(str).str.replace(' ', '2279')
    dataset['TotalCharges'] = dataset['TotalCharges'].replace('nan', '2279')
    dataset['TotalCharges'] = dataset['TotalCharges'].astype(float)

    # Contract is an important feature in the model and can't be null
    if dataset['Contract'].isnull().any():
        raise ValueError("Contract column contains null values.")

    dataset['PhoneService'] = dataset['PhoneService'].fillna('No')
    dataset['tenure'] = dataset['tenure'].fillna(dataset['tenure'].mean())

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