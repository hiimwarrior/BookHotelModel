import mlflow
import mlflow.sklearn
from modelling.mlflow_config import setup_mlflow_experiment
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from utils.models import save_model

def run_experiment():
    # Set up MLflow experiment
    setup_mlflow_experiment("Iris_Classification_Experiment")

    # Load dataset
    data = load_iris()
    X = data.data
    y = data.target

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train the model
    model = RandomForestClassifier(n_estimators=10)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    
    # Log the experiment and model in MLflow
    with mlflow.start_run() as run:
        # Log parameters and metrics
        mlflow.log_param("n_estimators", 10)
        mlflow.log_metric("accuracy", accuracy)
        
        # Log the model
        model_path = "model"  # Name for the model directory
        mlflow.sklearn.log_model(model, model_path)
        
        # Register the model
        model_uri = f"runs:/{run.info.run_id}/{model_path}"
        model_name = "Iris_Classifier_Model"
        mlflow.register_model(model_uri, model_name)
        
        # Output the results
        print(f"Model accuracy: {accuracy}")
        print(f"Run ID: {run.info.run_id}")
        print(f"Model URI: {model_uri}")

    # Save the model to disk
    model_version = "v1"  # You can generate versions dynamically if needed
    save_model(model, "RandomForestClassifier", model_version)
    
if __name__ == "__main__":
    run_experiment()
