import os
import json
import requests
from .config import DATASETS

# Load Schema function
def load_schema(schema_path):
    with open(schema_path, 'r') as file:
        schema = json.load(file)
    return schema

# Function to check if CSV file is empty
def is_csv_empty(file_path: str) -> bool:
    return not os.path.exists(file_path) or os.path.getsize(file_path) == 0

# Function to save data to CSV
def save_to_csv(df, file_path='../data/processed/clean_hotel_bookings.csv'):
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

def download_dataset(dataset_key: str) -> None:
    """
    Download a dataset based on the key provided in the configuration.

    Args:
        dataset_key (str): The key for the dataset to be downloaded, which should be in the DATASETS dictionary.
    """
    if dataset_key not in DATASETS:
        raise ValueError(f"Dataset '{dataset_key}' not found in configuration.")
    
    dataset = DATASETS[dataset_key]
    url = dataset['url']
    output_path = dataset['destination']
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_path, 'wb') as file:
                file.write(response.content)
            print(f"Data downloaded and saved in {output_path}")
        else:
            raise Exception(f"Failed to download data. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        raise