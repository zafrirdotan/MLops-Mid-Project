import pandas as pd
import json
import os

def get_training_stats(input_csv_path, output_json_path):
    required_columns = ['TotalCharges', 'Contract', 'PhoneService', 'tenure']
    df = pd.read_csv(input_csv_path, usecols=required_columns)

    stats = {}
    for col in df.columns:
        if df[col].dtype == 'object':
            stats[col] = {
                'unique_values': int(df[col].nunique()),
                'most_frequent_value': str(df[col].mode()[0]) if not df[col].mode().empty else None,
                'missing_values': int(df[col].isnull().sum())
            }
        else:
            stats[col] = {
                'mean': float(df[col].mean()) if pd.notnull(df[col].mean()) else None,
                'std_dev': float(df[col].std()) if pd.notnull(df[col].std()) else None,
                'min': float(df[col].min()) if pd.notnull(df[col].min()) else None,
                'max': float(df[col].max()) if pd.notnull(df[col].max()) else None,
                'missing_values': int(df[col].isnull().sum())
            }

    if os.path.exists(output_json_path):
        os.remove(output_json_path)

    with open(output_json_path, 'w') as f:
        json.dump(stats, f, indent=2)

if __name__ == "__main__":
    input_csv_path = 'input_mock_data/original_dataset.csv'
    output_json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/training_stats.json'))
    get_training_stats(input_csv_path, output_json_path)