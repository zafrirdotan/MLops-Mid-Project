import pandas as pd
import sys
import os
import logging

from sklearn.ensemble import RandomForestClassifier

# Add the root directory to sys.path, this is used to get the common folder in venv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.model import load_model
from common.preprocessing import preprocess_data
from common.prediction import predict
from data_drift import check_data_drift, load_training_stats

from db import get_mongo_collection
from typing import Generator, List, Any
from pymongo.collection import Collection
from common.dto.Customer import CustomerDTO  # Import your DTO
from common.logging import setup_logging

setup_logging( "batch_runner.log")

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/churn_model.pickle'))

def get_paginated_data(collection: Collection, page_size: int = 1000) -> Generator[List[CustomerDTO], None, None]:
    """
    Generator to yield paginated data from a MongoDB collection.
    
    Parameters:
    - collection: The MongoDB collection to query.
    - page_size: Number of documents to return per page.
    
    Yields:
    - List of documents from the collection.
    """
    total_documents = collection.count_documents({})
    for skip in range(0, total_documents, page_size):
        yield list(collection.find().skip(skip).limit(page_size))

def preprocess_and_predict(data_set: pd.DataFrame, model: RandomForestClassifier) -> pd.DataFrame:
    """
    Preprocess the dataset and make predictions using the loaded model.
    
    Parameters:
    - data_set: DataFrame containing the raw data.
    
    Returns:
    - DataFrame with predictions.
    """
    processed_data = preprocess_data(data_set)
    prediction = predict(model, processed_data)
        
    return pd.DataFrame({
        'customerID': processed_data['customerID'],
        'willDrop': prediction,
        'date': pd.Timestamp.now()
    })


def main():

    logging.info("Starting batch processing...")

    collection = get_mongo_collection("raw_inputs")
    if collection.count_documents({}) == 0:
        logging.error("No data found in the 'raw_inputs' collection. Please import data before running the batch process.")
        sys.exit(1)

    page_size = 1000

    model = load_model(model_path)

    training_stats_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/training_stats.json'))

    training_stats = load_training_stats(training_stats_path)
    
    output_collection = get_mongo_collection("predictions")

    for raw_docs in get_paginated_data(collection, page_size):
        if not raw_docs:
            continue
        typed_docs = [CustomerDTO(**doc).model_dump(by_alias=True) for doc in raw_docs]
        data_set = pd.DataFrame(typed_docs)

        check_data_drift(data_set, training_stats, threshold=0.1)

        prediction_to_save = preprocess_and_predict(data_set, model)
        
        output_collection.insert_many(prediction_to_save.to_dict('records'))
        logging.info(f"Processed and saved {len(prediction_to_save)} predictions.")
        print(f"Processed and saved {len(prediction_to_save)} predictions.")

    logging.info("Batch processing completed successfully.")
    print("Batch processing completed successfully.")

if __name__ == "__main__":
    main()
# This script processes data in batches from a MongoDB collection, makes predictions using a pre-trained model, and saves the results back to another MongoDB collection.
# It uses a paginated approach to handle large datasets efficiently.
# The script assumes the existence of a MongoDB database and collections, as well as a pre-trained model saved in a specified path.
# Ensure the necessary modules are installed and available in your environment.