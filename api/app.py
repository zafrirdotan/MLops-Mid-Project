import pandas as pd
from flask import Flask, jsonify, request
import os
import sys

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.model import load_model
from common.preprocessing import preprocess_data
from common.prediction import predict

app = Flask(__name__)

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/churn_model.pickle'))
model = load_model(model_path)

@app.route('/predict', methods=['POST'])
def predict_row():
    # Get JSON data as DTO
    data = request.get_json()
    print('DEBUG: data received:', data)
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    # Convert to DataFrame
    row = pd.DataFrame([data])
    print('DEBUG: DataFrame columns:', row.columns.tolist())
    try:
        processed = preprocess_data(row)
        pred = predict(model, processed)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'prediction': int(pred[0])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


