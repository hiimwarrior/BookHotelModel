import os
import json

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