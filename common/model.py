import pickle

def load_model(model_path):
    """
    Load the pre-trained model from the specified path.
    
    Args:
        model_path (str): Path to the model file.
        
    Returns:
        model: The loaded machine learning model.
    """
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model