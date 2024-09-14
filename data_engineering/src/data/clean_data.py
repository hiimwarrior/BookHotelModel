import pandas as pd
import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import os

# Function to process and clean data
def process_data():
    # Cargar el dataset crudo
    df = pd.read_csv('data/raw/hotel_bookings.csv', parse_dates=['reservation_status_date'])

    # Proceso de limpieza de datos
    df[['agent','company']] = df[['agent','company']].fillna(0)
    df['country'] = df['country'].fillna(df.country.mode()[0])
    df['children'] = df['children'].fillna(df.children.mode()[0])

    # Tipos de datos transformados
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
        'reserved_room_type': 'str',
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

    # Crear la columna de fecha completa
    df_transformado['arrival_date'] = pd.to_datetime(df_transformado['arrival_date_year'].astype(str) + '-' + 
                                        df_transformado['arrival_date_month'].astype(str) + '-' + 
                                        df_transformado['arrival_date_day_of_month'].astype(str))

    # Día de la semana de llegada
    df_transformado['arrival_day_of_week'] = df_transformado['arrival_date'].dt.dayofweek

    # Mes de llegada
    df_transformado['arrival_month'] = df_transformado['arrival_date'].dt.month

    # Definir las estaciones del año
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Invierno'
        elif month in [3, 4, 5]:
            return 'Primavera'
        elif month in [6, 7, 8]:
            return 'Verano'
        else:
            return 'Otoño'

    df_transformado['season'] = df_transformado['arrival_month'].apply(get_season)

    # Indicador de fin de semana
    df_transformado['is_weekend'] = df_transformado['arrival_day_of_week'].isin([5, 6]).astype(int)

    # Total de noches
    df_transformado['total_nights'] = df_transformado['stays_in_weekend_nights'] + df_transformado['stays_in_week_nights']

    # Tasa de cancelación por tipo de cliente
    cancellation_rate = df_transformado.groupby('customer_type')['is_canceled'].mean()
    df_transformado['customer_type_cancellation_rate'] = df_transformado['customer_type'].map(cancellation_rate)

    # Promedio de ADR por tipo de habitación
    avg_adr_by_room = df_transformado.groupby('reserved_room_type')['adr'].mean()
    df_transformado['avg_adr_for_room_type'] = df_transformado['reserved_room_type'].map(avg_adr_by_room)

    # Total de huéspedes
    df_transformado['total_guests'] = df_transformado['adults'] + df_transformado['children'] + df_transformado['babies']

    # Interacción entre tipo de habitación y temporada
    df_transformado['room_season'] = df_transformado['reserved_room_type'] + '_' + df_transformado['season']

    # Interacción entre tipo de cliente y temporada
    df_transformado['customer_season'] = df_transformado['customer_type'].astype(str) + '_' + df_transformado['season'].astype(str)

    # Ratio de ADR respecto al promedio de ADR para ese tipo de habitación
    df_transformado['adr_ratio'] = df_transformado['adr'] / df_transformado['avg_adr_for_room_type']

    # Diferencia entre la fecha de reserva y la fecha de llegada (lead time en días)
    df_transformado['booking_date'] = df_transformado['arrival_date'] - pd.to_timedelta(df_transformado['lead_time'], unit='D')
    df_transformado['booking_to_arrival_weeks'] = (df_transformado['arrival_date'] - df_transformado['booking_date']).dt.days // 7

    # Es una reserva de última hora
    df_transformado['is_last_minute'] = (df_transformado['lead_time'] < 7).astype(int)

    # Total de servicios especiales solicitados
    df_transformado['total_special_requests'] = df_transformado['required_car_parking_spaces'] + df_transformado['total_of_special_requests']

    # Es temporada alta
    high_season_months = [6, 7, 8, 12]
    df_transformado['is_high_season'] = df_transformado['arrival_month'].isin(high_season_months).astype(int)

    return df_transformado

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