import os
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.preprocessing import StandardScaler, OneHotEncoder
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

    df_transformado = df.astype({
        'hotel': 'category',
        'is_canceled': 'int64',
        'lead_time': 'int64',
        'arrival_date_year': 'category',
        'arrival_date_month': 'category',
        'arrival_date_week_number': 'int64',
        'arrival_date_day_of_month': 'int64',
        'stays_in_weekend_nights': 'int64',
        'stays_in_week_nights': 'int64',
        'adults': 'int64',
        'children': 'int64',
        'babies': 'int64',
        'meal': 'category',
        'country': 'category',
        'market_segment': 'category',
        'distribution_channel': 'category',
        'is_repeated_guest': 'category',
        'previous_cancellations': 'int64',
        'previous_bookings_not_canceled': 'int64',
        'reserved_room_type': 'category',
        'assigned_room_type': 'category',
        'booking_changes': 'int64',
        'deposit_type': 'category',
        'agent': 'category',
        'company': 'category',
        'days_in_waiting_list': 'int64',
        'customer_type': 'category',
        'adr': 'float',
        'required_car_parking_spaces': 'int64',
        'total_of_special_requests': 'int64',
        'reservation_status': 'category',
        'reservation_status_date': 'datetime64[ns]'
    })
    df_transformado.info()
    df = df_transformado

    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])

    # Extraer características de fecha (año, mes, día)
    df['reservation_year'] = df['reservation_status_date'].dt.year
    df['reservation_month'] = df['reservation_status_date'].dt.month
    df['reservation_day'] = df['reservation_status_date'].dt.day

    # Ahora podemos eliminar la columna de fecha original si ya no es necesaria
    df.drop('reservation_status_date', axis=1, inplace=True)

    df.drop('arrival_date', axis=1, inplace=True)
    df.drop('arrival_day_of_week', axis=1, inplace=True)
    df.drop('arrival_month', axis=1, inplace=True)
    df.drop('season', axis=1, inplace=True)
    df.drop('is_weekend', axis=1, inplace=True)
    df.drop('total_nights', axis=1, inplace=True)
    df.drop('customer_type_cancellation_rate', axis=1, inplace=True)
    df.drop('avg_adr_for_room_type', axis=1, inplace=True)
    df.drop('total_guests', axis=1, inplace=True)
    df.drop('room_season', axis=1, inplace=True)
    df.drop('customer_season', axis=1, inplace=True)
    df.drop('booking_date', axis=1, inplace=True)
    df.drop('booking_to_arrival_weeks', axis=1, inplace=True)
    df.drop('is_last_minute', axis=1, inplace=True)
    df.drop('total_special_requests', axis=1, inplace=True)
    df.drop('is_high_season', axis=1, inplace=True)

    # Identificar las columnas categóricas que deben ser codificadas
    categorical_cols = ['hotel', 'arrival_date_year', 'arrival_date_month', 'meal', 'country', 'market_segment', 'distribution_channel', 'is_repeated_guest', 'market_segment', 
                        'customer_type', 'reserved_room_type', 'assigned_room_type','deposit_type','agent','company','reservation_status']

    # Aplicar OneHotEncoding a las columnas categóricas usando get_dummies()
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Verificar que no hay variables categóricas sin codificar
    # print(df_encoded.dtypes)

    # Identificar columnas numéricas
    numerical_cols = ['arrival_date_week_number','arrival_date_day_of_month','stays_in_weekend_nights','stays_in_week_nights',
                    'adults','children','babies','previous_cancellations','previous_bookings_not_canceled','booking_changes',
                    'days_in_waiting_list','adr','required_car_parking_spaces','total_of_special_requests']

    # Escalar las variables numéricas
    scaler = StandardScaler()
    df_encoded[numerical_cols] = scaler.fit_transform(df_encoded[numerical_cols])


    X = df_encoded.drop('is_canceled', axis=1)
    y = df_encoded['is_canceled']

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
