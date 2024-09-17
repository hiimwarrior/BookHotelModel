import os
from .models import save_model, load_model

def test_save_model():
    model = "test_model"
    model_name = "test_model"
    version = "v1"
    
    save_model(model, model_name, version)
    
    model_path = os.path.join("src/model_output", model_name, f"{model_name}_{version}.pkl")
    assert os.path.exists(model_path), f"Expected model file {model_path} does not exist."

def test_load_model():
    model = "test_model"
    model_name = "test_model"
    version = "v1"
    
    save_model(model, model_name, version)
    
    loaded_model = load_model(model_name, version)
    assert loaded_model == model, "Loaded model does not match the saved model."
