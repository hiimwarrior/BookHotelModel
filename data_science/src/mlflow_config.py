import os
import mlflow
from pathlib import Path

def setup_mlflow_experiment(experiment_name):
    # Get the current directory and its parent
    current_dir = Path(__file__).resolve().parent
    base_dir = current_dir.parent

    # Define the path for mlruns
    mlruns_dir = base_dir / "mlruns"
    
    # Create the mlruns directory if it doesn't exist
    mlruns_dir.mkdir(parents=True, exist_ok=True)
    
    # Set the tracking URI
    tracking_uri = f"file://{mlruns_dir}"
    mlflow.set_tracking_uri(tracking_uri)
    
    # Set the experiment
    mlflow.set_experiment(experiment_name)
