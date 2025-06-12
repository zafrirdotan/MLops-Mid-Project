import pandas as pd
from flask import Flask, jsonify, request
import os
import sys

# Add the root directory to sys.path, this is used to get the common folder in venv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.dto.Customer import CustomerDTO
from common.model import load_model
from common.preprocessing import preprocess_data
from common.prediction import predict

app = Flask(__name__)

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/churn_model.pickle'))

model = load_model(model_path)

@app.route('/predict', methods=['POST'])
def predict_row():
    # Get JSON data as DTO
    json_data = request.get_json()
    
    # Validate input data
    if not json_data:
        return jsonify({'error': 'No input data provided'}), 400
    
    # Convert JSON data to CustomerDTO and then to a dictionary 
    data = CustomerDTO(**json_data).__dict__
      
    # Create a DataFrame from the data
    row = pd.DataFrame([data])

    # Preprocess the data and make predictions
    try:
        # Preprocess input data
        processed = preprocess_data(row)
        # Make prediction
        prediction = predict(model, processed)[0]
        # Prepare response with selected fields and convert NumPy types to native Python types
        processed_data = processed.iloc[0].to_dict()
        def to_py(val):
            if hasattr(val, "item"):
                return val.item()
            return val
        response = {
            'prediction': to_py(prediction),
            'TotalCharges': to_py(processed_data.get('TotalCharges')),
            'contract_type': to_py(processed_data.get('Contract')),
            'PhoneService': to_py(processed_data.get('PhoneService')),
            'tenure': to_py(processed_data.get('tenure'))
        }
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    # Extract relevant fields for response
 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
