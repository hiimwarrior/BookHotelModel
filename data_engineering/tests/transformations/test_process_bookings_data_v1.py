import pytest
from unittest.mock import patch
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from io import StringIO

# Asumiendo que process_bookings_data_v1 está en el archivo process.py
from src.transformations.process_bookings_data_v1 import process_bookings_data_v1

# Datos de prueba para el archivo CSV
csv_data = StringIO("""
hotel,is_canceled,lead_time,arrival_date_year,arrival_date_month,arrival_date_week_number,arrival_date_day_of_month,stays_in_weekend_nights,stays_in_week_nights,adults,children,babies,meal,country,market_segment,distribution_channel,is_repeated_guest,previous_cancellations,previous_bookings_not_canceled,reserved_room_type,assigned_room_type,booking_changes,deposit_type,agent,company,days_in_waiting_list,customer_type,adr,required_car_parking_spaces,total_of_special_requests,reservation_status,reservation_status_date
Resort Hotel,0,342,2015,July,27,1,0,0,2,0,0,BB,PRT,Direct,Direct,0,0,0,C,C,3,No Deposit,NULL,NULL,0,Transient,0,0,0,Check-Out,7/1/2015
Resort Hotel,0,737,2015,July,27,1,0,0,2,0,0,BB,PRT,Direct,Direct,0,0,0,C,C,4,No Deposit,NULL,NULL,0,Transient,0,0,0,Check-Out,7/1/2015
""")


def test_process_bookings_data_v1():
    # Mock de load_schema para cargar el esquema JSON
    with patch('src.transformations.process_bookings_data_v1.load_schema') as mock_load_schema:
        mock_load_schema.return_value = {
            'hotel': 'category',
            'arrival_date_year': 'int64',
            'arrival_date_month': 'category',
            'reservation_status_date': 'object',
            'agent': 'float64',
            'company': 'float64',
            'country': 'category',
            'children': 'float64',
            'arrival_date_week_number': 'int64',
            'arrival_date_day_of_month': 'int64',
            'stays_in_weekend_nights': 'int64',
            'stays_in_week_nights': 'int64',
            'adults': 'int64',
            'babies': 'int64',
            'previous_cancellations': 'int64',
            'previous_bookings_not_canceled': 'int64',
            'booking_changes': 'int64',
            'days_in_waiting_list': 'int64',
            'adr': 'float64',
            'required_car_parking_spaces': 'int64',
            'total_of_special_requests': 'int64'
        }
        mock_df = pd.read_csv(csv_data)
        
        # Mock de pd.read_csv para cargar el CSV en memoria
        with patch('src.transformations.process_bookings_data_v1.pd.read_csv', return_value=mock_df):
            # Ejecutar la función de procesamiento
            result = process_bookings_data_v1()
            # TODO fix rest of tests
            # Verificar que las columnas categóricas fueron codificadas
            # assert 'hotel_Resort Hotel' in result.columns
            # assert 'arrival_date_month_July' in result.columns

            # # Verificar que las columnas numéricas fueron escaladas correctamente
            # numerical_cols = ['arrival_date_week_number','arrival_date_day_of_month','stays_in_weekend_nights','stays_in_week_nights',
            #                 'adults','children','babies','previous_cancellations','previous_bookings_not_canceled','booking_changes',
            #                 'days_in_waiting_list','adr','required_car_parking_spaces','total_of_special_requests']
            # scaler = StandardScaler()
            # expected_values = scaler.fit_transform(pd.DataFrame({
            #     'arrival_date_week_number': [27, 32],
            #     'arrival_date_day_of_month': [1, 2],
            #     'stays_in_weekend_nights': [1, 2],
            #     'stays_in_week_nights': [1, 2],
            #     'adults': [1, 2],
            #     'children': [0, 1],
            #     'babies': [0, 0],
            #     'previous_cancellations': [0, 0],
            #     'previous_bookings_not_canceled': [0, 0],
            #     'booking_changes': [0, 0],
            #     'days_in_waiting_list': [200, 300],
            #     'adr': [100, 50],
            #     'required_car_parking_spaces': [0, 1],
            #     'total_of_special_requests': [0, 1]
            # }))
            # np.testing.assert_array_almost_equal(result[numerical_cols].values, expected_values)

            # # Verificar que la columna 'reservation_status_date' fue eliminada
            # assert 'reservation_status_date' not in result.columns

            # # Verificar que se han añadido las nuevas columnas de fecha
            # assert 'reservation_year' in result.columns
            # assert 'reservation_month' in result.columns
            # assert 'reservation_day' in result.columns

if __name__ == '__main__':
    pytest.main()
