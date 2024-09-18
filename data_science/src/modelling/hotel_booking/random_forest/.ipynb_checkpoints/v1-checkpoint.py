import os
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import argparse
from modelling.mlflow_config import setup_mlflow_experiment
from utils.models import save_model

def run_random_forest_experiment(data_version, model_version):
    # Set up MLflow experiment
    setup_mlflow_experiment("Hotel_Bookings_Random_Forest_Experiment")

    # Construct the path to the dataset
    dataset_filename = f"clean_hotel_bookings_v{data_version}.csv"
    base_dir = os.path.dirname(__file__)
    
    # Construye la ruta absoluta hacia el archivo de datos
    data_path = os.path.abspath(os.path.join(base_dir, '../../../../../data/processed', dataset_filename))
    
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}")
        return

    # Load and prepare data
    df = pd.read_csv(data_path)
    X = df.drop('is_canceled', axis=1)
    y = df['is_canceled']

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the RandomForest model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    with mlflow.start_run() as run:
        rf_model.fit(X_train, y_train)
        
        # Make predictions
        y_pred_rf = rf_model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred_rf)
        precision = precision_score(y_test, y_pred_rf)
        recall = recall_score(y_test, y_pred_rf)
        f1 = f1_score(y_test, y_pred_rf)
        roc_auc = roc_auc_score(y_test, y_pred_rf)
        
        # Print evaluation metrics
        print('Random Forest Model:')
        print(f'Accuracy: {accuracy}')
        print(f'Precision: {precision}')
        print(f'Recall: {recall}')
        print(f'F1 Score: {f1}')
        print(f'ROC AUC Score: {roc_auc}')

        # Log parameters and metrics to MLflow
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("roc_auc", roc_auc)
        
        # Log the model to MLflow
        model_path = "model"
        mlflow.sklearn.log_model(rf_model, model_path)
        
        # Register the model
        model_uri = f"runs:/{run.info.run_id}/{model_path}"
        model_name = f"Hotel_Bookings_Random_Forest_Model_{model_version}"
        mlflow.register_model(model_uri, model_name)
        
        print(f"Model URI: {model_uri}")

        # Save the model to disk
        model_version = "v1"  # You can generate versions dynamically if needed
        save_model(rf_model, "RandomForestClassifier", model_version)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Random Forest Experiment.')
    parser.add_argument('--data', type=str, required=True, help='Version of the dataset to use')
    parser.add_argument('--version', type=str, required=True, help='Version of the model')
    
    args = parser.parse_args()
    run_random_forest_experiment(args.data, args.version)
