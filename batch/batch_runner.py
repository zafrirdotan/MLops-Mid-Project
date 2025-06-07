import pandas as pd
import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.model import load_model
from common.preprocessing import preprocess_data
from common.prediction import predict

from db import get_mongo_collection

# Load the dataset from mongoDB
collection = get_mongo_collection("raw_inputs")
if collection.count_documents({}) == 0:
    print("No data found in the MongoDB collection 'raw_inputs'.")
    sys.exit(1)
    
# Convert MongoDB collection to DataFrame
data_set = pd.DataFrame(list(collection.find()))

processed_data = preprocess_data(data_set)

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/churn_model.pickle'))
model = load_model(model_path)

prediction = predict(model, processed_data)

# Print the prediction results
print(prediction)

# Combine customerID with predictions
prediction_to_save = pd.DataFrame({
    'customerID': data_set['customerID'],
    'willDrop': prediction
})

# Save the predictions to MongoDB
output_collection = get_mongo_collection("predictions")
if output_collection.count_documents({}) > 0:
    output_collection.drop()  # Clear existing predictions
output_collection.insert_many(prediction_to_save.to_dict('records'))
print("Predictions saved to MongoDB collection 'predictions'.")