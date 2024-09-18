from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import os

# Function to check if CSV file is empty
def is_csv_empty(file_path: str) -> bool:
    return not os.path.exists(file_path) or os.path.getsize(file_path) == 0

# Function to check if table is empty in the database
def is_table_empty(engine: Engine, table_name: str) -> bool:
    with engine.connect() as connection:
        result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()
    return count == 0

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