import pandas as pd
import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import os

# Function to process and clean data
def process_data():
    # Load the raw dataset
    df = pd.read_csv('data/raw/hotel_bookings.csv')

    # Data cleaning process
    df.drop(['agent', 'company', 'reservation_status_date'], axis=1, inplace=True)
    df['children'].fillna(0, inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df['meal'].fillna('SC', inplace=True)
    df = pd.get_dummies(df, columns=['hotel', 'arrival_date_month', 'meal', 'country', 'market_segment', 'distribution_channel', 'reserved_room_type', 'deposit_type', 'customer_type'])
    df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['total_guests'] = df['adults'] + df['children'] + df['babies']
    df = df[df['adults'] + df['children'] + df['babies'] > 0]

    return df

# Function to save data to CSV
def save_to_csv(df, file_path='data/processed/clean_hotel_bookings.csv'):
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

# Function to check if table is empty in the database
def is_table_empty(engine: Engine, table_name: str) -> bool:
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()
    return count == 0

# Function to check if CSV file is empty
def is_csv_empty(file_path: str) -> bool:
    return not os.path.exists(file_path) or os.path.getsize(file_path) == 0

# Function to save data to MySQL database
def save_to_db(df, db_url='mysql+pymysql://user:password@localhost:3307/hotel_booking_db', version='1'):
    table_name = f'hotel_bookings_v{version}'
    engine = create_engine(db_url)

    if is_table_empty(engine, table_name) or is_csv_empty('data/processed/clean_hotel_bookings.csv'):
        # If table or CSV is empty, drop existing table and insert new data
        with engine.connect() as connection:
            connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
        df.to_sql(table_name, con=engine, index=False, if_exists='replace')
        print(f"Data saved to MySQL database in table '{table_name}'")
    else:
        print(f"Table '{table_name}' already contains data. No new data inserted.")

def main():
    parser = argparse.ArgumentParser(description='Process and clean hotel bookings data.')
    parser.add_argument('--destination', choices=['csv', 'db'], default='csv',
                        help='Specify the destination for the processed data. Options are "csv" or "db". Default is "csv".')
    parser.add_argument('--version', default='1',
                        help='Specify the version of the transformation. Default is "1".')
    args = parser.parse_args()

    # Process the data
    df = process_data()

    # Save the data based on the destination parameter
    if args.destination == 'csv':
        if is_csv_empty('data/processed/clean_hotel_bookings.csv'):
            save_to_csv(df)
        else:
            print("CSV file already contains data. No new data saved.")
    elif args.destination == 'db':
        save_to_db(df, version=args.version)

if __name__ == '__main__':
    main()
