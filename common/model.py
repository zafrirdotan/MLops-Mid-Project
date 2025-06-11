import pickle
from sklearn.ensemble import RandomForestClassifier
import logging

def load_model(model_path: str) -> RandomForestClassifier:
    """
    Load the pre-trained model from the specified path.
    
    Args:
        model_path (str): Path to the model file.
        
    Returns:
        model: The loaded machine learning model.
    """
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        logging.error(f"Failed to load model from {model_path}: {e}")
        raise