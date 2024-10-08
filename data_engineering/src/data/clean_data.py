import pandas as pd
import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import os
from src.utils.file import is_csv_empty

# Function to process and clean data
def process_data():
    dataset_filename="hotel_bookings.csv"
    base_dir = os.path.dirname(__file__)
    # Construye la ruta absoluta hacia el archivo de datos
    data_path = os.path.abspath(os.path.join(base_dir, '../../../data/raw', dataset_filename))
    df = pd.read_csv(data_path, parse_dates=['reservation_status_date'])

    # Proceso de limpieza de datos
    df[['agent','company']] = df[['agent','company']].fillna(0)
    df['country'] = df['country'].fillna(df.country.mode()[0])
    df['children'] = df['children'].fillna(df.children.mode()[0])

    # Crear una columna de fecha completa
    df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' + 
                                        df['arrival_date_month'].astype(str) + '-' + 
                                        df['arrival_date_day_of_month'].astype(str))

    # Día de la semana de llegada
    df['arrival_day_of_week'] = df['arrival_date'].dt.dayofweek

    # Mes de llegada
    df['arrival_month'] = df['arrival_date'].dt.month

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

    df['season'] = df['arrival_month'].apply(get_season)

    # Indicador de fin de semana
    df['is_weekend'] = df['arrival_day_of_week'].isin([5, 6]).astype(int)

    # Total de noches
    df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']

    # Tasa de cancelación por tipo de cliente
    cancellation_rate = df.groupby('customer_type')['is_canceled'].mean()
    df['customer_type_cancellation_rate'] = df['customer_type'].map(cancellation_rate)

    # Promedio de ADR por tipo de habitación
    avg_adr_by_room = df.groupby('reserved_room_type')['adr'].mean()
    df['avg_adr_for_room_type'] = df['reserved_room_type'].map(avg_adr_by_room)

    # Total de huéspedes
    df['total_guests'] = df['adults'] + df['children'] + df['babies']

    # Interacción entre tipo de habitación y temporada
    df['room_season'] = df['reserved_room_type'] + '_' + df['season']

    # Interacción entre tipo de cliente y temporada
    df['customer_season'] = df['customer_type'].astype(str) + '_' + df['season'].astype(str)

    # Ratio de ADR respecto al promedio de ADR para ese tipo de habitación

    df['adr_ratio'] = df['adr'] / df['avg_adr_for_room_type']

    # Diferencia entre la fecha de reserva y la fecha de llegada (lead time en días)
    df['booking_date'] = df['arrival_date'] - pd.to_timedelta(df['lead_time'], unit='D')
    df['booking_to_arrival_weeks'] = (df['arrival_date'] - df['booking_date']).dt.days // 7

    # Es una reserva de última hora
    df['is_last_minute'] = (df['lead_time'] < 7).astype(int)

    # Total de servicios especiales solicitados
    df['total_special_requests'] = df['required_car_parking_spaces'] + df['total_of_special_requests']

    # Es temporada alta
    high_season_months = [6, 7, 8, 12]
    df['is_high_season'] = df['arrival_month'].isin(df).astype(int)


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
        'reservation_status_date': 'datetime64[ns]',
        'arrival_date': 'datetime64[ns]',
        'arrival_day_of_week': 'int64',
        'arrival_month': 'int64',
        'season': 'category',
        'is_weekend': 'int64',
        'total_nights': 'int64',
        'customer_type_cancellation_rate': 'float64',
        'avg_adr_for_room_type': 'float64',
        'total_guests': 'int64',
        'room_season': 'category',
        'customer_season': 'category',
        'booking_date': 'datetime64[ns]',
        'booking_to_arrival_weeks': 'int64',
        'is_last_minute': 'int64',
        'total_special_requests': 'int64',
        'is_high_season': 'int64'
    })

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