import pandas as pd
import json
import os
import sys

# Add the root directory to sys.path, this is used to get the common folder in venv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.preprocessing import preprocess_data

def get_training_stats(input_csv_path, output_json_path):
    required_columns = ['TotalCharges', 'Contract', 'PhoneService', 'tenure']
    df = pd.read_csv(input_csv_path, usecols=required_columns)

    processed_data = preprocess_data(df)

    stats = {}
    for col in processed_data.columns:
        if processed_data[col].dtype == 'object':
            stats[col] = {
                'unique_values': int(processed_data[col].nunique()),
                'most_frequent_value': str(processed_data[col].mode()[0]) if not processed_data[col].mode().empty else None,
                'missing_values': int(processed_data[col].isnull().sum())
            }
        else:
            stats[col] = {
                'mean': float(processed_data[col].mean()) if pd.notnull(processed_data[col].mean()) else None,
                'std_dev': float(processed_data[col].std()) if pd.notnull(processed_data[col].std()) else None,
                'min': float(processed_data[col].min()) if pd.notnull(processed_data[col].min()) else None,
                'max': float(processed_data[col].max()) if pd.notnull(processed_data[col].max()) else None,
                'missing_values': int(processed_data[col].isnull().sum())
            }

    if os.path.exists(output_json_path):
        os.remove(output_json_path)

    with open(output_json_path, 'w') as f:
        json.dump(stats, f, indent=2)

if __name__ == "__main__":
    input_csv_path = 'input_mock_data/original_dataset.csv'
    output_json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/training_stats.json'))
    get_training_stats(input_csv_path, output_json_path)
    # Gets the training stats from the original dataset and saves them to a JSON file
    print(f"Training stats saved to {output_json_path}")