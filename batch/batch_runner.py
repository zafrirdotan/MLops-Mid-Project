import pandas as pd
import sys
import os

from sklearn.ensemble import RandomForestClassifier

# Add the root directory to sys.path, this is used to get the common folder in venv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.model import load_model
from common.preprocessing import preprocess_data
from common.prediction import predict

from db import get_mongo_collection
from typing import Generator, List, Any
from pymongo.collection import Collection
from common.dto.Customer import CustomerDTO  # Import your DTO

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
    collection = get_mongo_collection("raw_inputs")
    if collection.count_documents({}) == 0:
        print("No data found in the MongoDB collection 'raw_inputs'.")
        sys.exit(1)

    page_size = 1000

    model = load_model(model_path)
    
    output_collection = get_mongo_collection("predictions")

    for raw_docs in get_paginated_data(collection, page_size):
        if not raw_docs:
            continue
        typed_docs = [CustomerDTO(**doc).model_dump(by_alias=True) for doc in raw_docs]
        data_set = pd.DataFrame(typed_docs)

        prediction_to_save = preprocess_and_predict(data_set, model)
        
        output_collection.insert_many(prediction_to_save.to_dict('records'))
        print(f"Saved {len(prediction_to_save)} predictions to MongoDB collection 'predictions'.")

    print("All predictions saved.")

if __name__ == "__main__":
    main()
# This script processes data in batches from a MongoDB collection, makes predictions using a pre-trained model, and saves the results back to another MongoDB collection.
# It uses a paginated approach to handle large datasets efficiently.
# The script assumes the existence of a MongoDB database and collections, as well as a pre-trained model saved in a specified path.
# Ensure the necessary modules are installed and available in your environment.