import pytest
import pandas as pd
from clean_data import process_data

# Test para verificar si el procesamiento de los datos es correcto
def test_process_data():
    # Llama a la función process_data para obtener el dataframe procesado
    df = process_data()

    # Verifica que las columnas esperadas están presentes en el dataframe
    expected_columns = [
        'hotel', 'is_canceled', 'lead_time', 'arrival_date_year', 'arrival_date_month',
        'arrival_date_week_number', 'arrival_date_day_of_month', 'stays_in_weekend_nights',
        'stays_in_week_nights', 'adults', 'children', 'babies', 'meal', 'country', 'market_segment',
        'distribution_channel', 'is_repeated_guest', 'previous_cancellations', 'previous_bookings_not_canceled',
        'reserved_room_type', 'assigned_room_type', 'booking_changes', 'deposit_type', 'agent', 'company',
        'days_in_waiting_list', 'customer_type', 'adr', 'required_car_parking_spaces', 'total_of_special_requests',
        'reservation_status', 'reservation_status_date', 'arrival_date', 'arrival_day_of_week', 'arrival_month',
        'season', 'is_weekend', 'total_nights', 'customer_type_cancellation_rate', 'avg_adr_for_room_type', 
        'total_guests', 'room_season', 'customer_season', 'adr_ratio', 'booking_date', 'booking_to_arrival_weeks', 
        'is_last_minute', 'total_special_requests', 'is_high_season'
    ]

    # Verifica que el dataframe tiene las columnas esperadas
    assert set(expected_columns).issubset(df.columns), "Faltan columnas esperadas en el DataFrame"

    # Verifica el tipo de datos de algunas columnas críticas
    assert pd.api.types.is_categorical_dtype(df['hotel']), "La columna 'hotel' no es de tipo categoría"
    assert pd.api.types.is_integer_dtype(df['is_canceled']), "La columna 'is_canceled' no es de tipo entero"
    assert pd.api.types.is_float_dtype(df['adr']), "La columna 'adr' no es de tipo float"
    assert pd.api.types.is_datetime64_any_dtype(df['reservation_status_date']), "La columna 'reservation_status_date' no es de tipo datetime"

    # Verifica que no haya valores nulos en columnas críticas
    assert df['hotel'].isnull().sum() == 0, "Existen valores nulos en la columna 'hotel'"
    assert df['is_canceled'].isnull().sum() == 0, "Existen valores nulos en la columna 'is_canceled'"

    # Verifica que las nuevas columnas derivadas de fechas sean correctas
    assert df['arrival_day_of_week'].max() <= 6, "arrival_day_of_week tiene valores fuera de rango"
    assert df['is_weekend'].isin([0, 1]).all(), "La columna 'is_weekend' tiene valores fuera de 0 o 1"
    
    # Test para asegurarse de que los valores de 'is_last_minute' están en el rango esperado
    assert df['is_last_minute'].isin([0, 1]).all(), "La columna 'is_last_minute' tiene valores fuera de 0 o 1"

