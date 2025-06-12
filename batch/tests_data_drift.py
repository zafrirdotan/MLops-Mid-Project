import pandas as pd
import sys
import os
import logging

# Add the root directory to sys.path, this is used to get the common folder in venv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.preprocessing import preprocess_data
from common.logging import setup_logging
setup_logging("tests_data_drift.log")

from data_drift import check_data_drift, load_training_stats

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/churn_model.pickle'))

def main():
    print("Starting data drift test...")

    df = pd.read_csv('input_mock_data/database_input2.csv')

    processed_data = preprocess_data(pd.DataFrame(df))

    training_stats_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/training_stats.json'))

    training_stats = load_training_stats(training_stats_path)

    check_data_drift(processed_data, training_stats, threshold=0.1)

if __name__ == "__main__":
    main()
# Test the data drift functionality