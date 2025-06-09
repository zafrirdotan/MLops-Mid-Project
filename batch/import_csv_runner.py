import pandas as pd
from db import get_mongo_collection
import sys
import os

# Add the root directory to sys.path, this is used to get the common folder in venv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.dto.Customer import CustomerDTO

def import_customers_from_csv(csv_path: str, collection_name: str = "raw_inputs"):
    df = pd.read_csv(csv_path)
    customers = [CustomerDTO(**row).model_dump(by_alias=True) for row in df.to_dict(orient="records")]
    collection = get_mongo_collection(collection_name)
    # Clear existing data in the collection
    if collection.count_documents({}) > 0:
        collection.drop()  # Clear existing data
    # Insert new data into the collection
    collection.insert_many(customers)
    print(f"✅ Imported {len(df)} records into {collection_name}.")
    print("✅ Total in Mongo now:", collection.count_documents({}))


def main():
    csv_path = 'input_mock_data/database_input.csv'
    import_customers_from_csv(csv_path)


if __name__ == "__main__":
    main()

