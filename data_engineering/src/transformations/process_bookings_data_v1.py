import pandas as pd
from sklearn.preprocessing import StandardScaler
from utils.file import load_schema

# Function to process and clean data
def process_bookings_data_v1():
    schema_path = 'data/schemas/hotel_bookings/hotel_bookings_schema_v1.json'
    hotel_bookings_schema_v1 = load_schema(schema_path)
    # Load the raw dataset
    transformed_df = pd.read_csv("../data/raw/hotel_bookings.csv")

    # Fill NA
    transformed_df[["agent", "company"]] = transformed_df[["agent", "company"]].fillna(0)
    transformed_df["country"] = transformed_df["country"].fillna(transformed_df.country.mode()[0])
    transformed_df["children"] = transformed_df["children"].fillna(transformed_df.children.mode()[0])
    transformed_df.isnull().sum().sort_values(ascending=False)
    
    # Transform the transformed_df to the proper data types
    transformed_df = transformed_df.astype(hotel_bookings_schema_v1) 

    # Data cleaning process
    transformed_df['reservation_status_date'] = pd.to_datetime(transformed_df['reservation_status_date'])

    # Extraer características de fecha (año, mes, día)
    transformed_df['reservation_year'] = transformed_df['reservation_status_date'].dt.year
    transformed_df['reservation_month'] = transformed_df['reservation_status_date'].dt.month
    transformed_df['reservation_day'] = transformed_df['reservation_status_date'].dt.day

    # Ahora podemos eliminar la columna de fecha original si ya no es necesaria
    transformed_df.drop('reservation_status_date', axis=1, inplace=True)
    
    # Identificar las columnas categóricas que deben ser codificadas
    categorical_cols = ['hotel', 'arrival_date_year', 'arrival_date_month', 'meal', 'country', 'market_segment', 'distribution_channel', 'is_repeated_guest', 'market_segment', 
                        'customer_type', 'reserved_room_type', 'assigned_room_type','deposit_type','agent','company','reservation_status']

    # Aplicar OneHotEncoding a las columnas categóricas usando get_dummies()
    df_encoded = pd.get_dummies(transformed_df, columns=categorical_cols, drop_first=True)

    # Identificar columnas numéricas
    numerical_cols = ['arrival_date_week_number','arrival_date_day_of_month','stays_in_weekend_nights','stays_in_week_nights',
                    'adults','children','babies','previous_cancellations','previous_bookings_not_canceled','booking_changes',
                    'days_in_waiting_list','adr','required_car_parking_spaces','total_of_special_requests']

    # Escalar las variables numéricas
    scaler = StandardScaler()
    df_encoded[numerical_cols] = scaler.fit_transform(df_encoded[numerical_cols])

    return df_encoded
