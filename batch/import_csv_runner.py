import pandas as pd
from db import get_mongo_collection
import sys
import os
import logging

# Add the root directory to sys.path, this is used to get the common folder in venv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.logging import setup_logging
setup_logging("import_csv_runner.log")

def import_customers_from_csv(csv_path: str, collection_name: str = "raw_inputs"):
    df = pd.read_csv(csv_path)
    if df.empty:
        print(f"No data found in {csv_path}.")
        logging.warning(f"No data found in {csv_path}.")
        return
    
    collection = get_mongo_collection(collection_name)
    # Clear existing data in the collection
    if collection.count_documents({}) > 0:
        collection.drop()  # Clear existing data
    # Insert new data into the collection
    collection.insert_many(df.to_dict(orient="records"))
    print(f"✅ Imported {len(df)} records into {collection_name} from {csv_path}.")
    print("✅ Total in Mongo now:", collection.count_documents({}))
    logging.info(f"Imported {len(df)} records into {collection_name} from {csv_path}.")


def main():
    csv_path = 'input_mock_data/original_dataset.csv'
    import_customers_from_csv(csv_path)
    
if __name__ == "__main__":
    main()
