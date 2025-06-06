import pandas as pd
from db import get_mongo_collection

df = pd.read_csv('input_mock_data/database_input.csv')

collection = get_mongo_collection("raw_inputs")
collection.insert_many(df.to_dict(orient="records"))

print(f"✅ Imported {len(df)} records into raw_inputs.")
print("✅ Total in Mongo now:", collection.count_documents({}))

