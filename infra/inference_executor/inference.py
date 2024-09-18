import os
import pandas as pd
import joblib
from sqlalchemy import create_engine
from integrations.s3_client import S3Client
from config import Config

# Load environment variables
config = Config()

def load_model():
    """Load model from either local filesystem or AWS S3."""
    if config.ENV == 'local':
        print("Loading model from local storage...")
        model_path = '/path/to/local/model/file.pkl'  # Update this path
    else:
        print("Loading model from S3...")
        s3_client = S3Client(
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region=config.AWS_REGION,
            bucket=config.S3_BUCKET
        )
        s3_client.download_model('model/model_file.pkl', 'local_model_file.pkl')
        model_path = 'local_model_file.pkl'

    # Load the model from model_path
    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)
    return model

def run_inference():
    # Load the model
    model = load_model()

    # Connect to the database
    print("Connecting to database...")
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()

    # Query records where possible_cancellation is NULL
    query = "SELECT * FROM reservations WHERE possible_cancellation IS NULL"
    df = pd.read_sql(query, connection)
    connection.close()

    # Prepare data for inference (assuming you need to preprocess it)
    # Replace 'features' with actual feature columns used in the model
    features = ['feature1', 'feature2']  # Update with actual feature columns
    X = df[features]

    # Run inference
    print("Running inference...")
    df['predicted_cancellation'] = model.predict(X)

    # Export results to CSV
    output_file = 'inference_results.csv'
    df.to_csv(output_file, index=False)
    print(f"Results exported to {output_file}")

if __name__ == "__main__":
    run_inference()