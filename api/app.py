import pandas as pd

from common.model import load_model
from common.preprocessing import preprocess_data
from common.prediction import predict


data_set = pd.read_csv('database_input.csv')

processed_data = preprocess_data(data_set)

model = load_model('model/model.pkl')

prediction = predict(model, processed_data)