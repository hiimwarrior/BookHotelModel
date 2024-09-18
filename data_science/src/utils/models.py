import joblib
import os

def save_model(model, model_name, version):
    """
    Save the model to a .pkl file in the output folder.
    """
    model_path = os.path.join("model_output", model_name, f"{model_name}_{version}.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

def load_model(model_name, version):
    """
    Load a model from a .pkl file.
    """
    model_path = os.path.join("model_output", model_name, f"{model_name}_{version}.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file {model_path} does not exist.")
    
    return joblib.load(model_path)
